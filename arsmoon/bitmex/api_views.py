# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from rest_framework import status, mixins
from rest_framework.response import Response
from arsmoon.bitmex.models import Order, Account
from rest_framework.viewsets import GenericViewSet
from arsmoon.bitmex.serializers import OrderSerializer


class OrderBitmexViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                        mixins.CreateModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    account = None

    def dispatch(self, request, *args, **kwargs):
        if 'account' in self.request.GET:
            self.account = Account.objects.filter(name=self.request.query_params['account']).first()
        return super().dispatch(request, *args, **kwargs)
        # if not self.account:
        #     return Response(
        #         {'error': 'No account with this name'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

    def get_queryset(self, *args, **kwargs):
        if self.account:
            return Order.objects.filter(account=self.account)
        return Order.objects.none()


    def retrieve(self, request, *args, **kwargs):
        """
        **Retrieve GeoPolygon instance with population data**

        ####**Allowed Methods**:
        ###### - GET

        #### **GET**:
        ###### URL: **api/geodata/geopolygons/{id}/**

        #### SUCCESS RESPONSE:
        ```json
            {
              "id": 25,
              "name": "Age checker",
              "polygon": "MULTIPOLYGON (((31.57745 4961782831211117, 31.57745361328125 49.33586159110413)))",
              "target_group": 1,
              "population_datas": [
                {
                  "female": 117005.231793478,
                  "male": 117912.501480582,
                  "sum": 231077,
                  "mean": 23.052374301676,
                  "max": 1364,
                  "min": 0,
                  "growth_rate": -0.545,
                  "hh_size": 3.2,
                  "Pyramids": [
                    {
                      "AgeGroup": "0_4",
                      "MalePop": 16405.0880827377,
                      "FemalePop": 16278.860384554,
                      "TotalPop": 32683.9484672917
                    },
                    {
                      "AgeGroup": "5_9",
                      "MalePop": 19596.8823065302,
                      "FemalePop": 19446.0955273704,
                      "TotalPop": 39042.9778339005
                    },
                    {
                      "AgeGroup": "10_14",
                      "MalePop": 16934.9737282001,
                      "FemalePop": 16804.6688746895,
                      "TotalPop": 33739.6426028896
                    },
                    {
                      "AgeGroup": "15_19",
                      "MalePop": 14250.8400644054,
                      "FemalePop": 14141.187934416,
                      "TotalPop": 28392.0279988214
                    },
                    {
                      "AgeGroup": "20_24",
                      "MalePop": 11869.6583400035,
                      "FemalePop": 11778.328018093,
                      "TotalPop": 23647.9863580965
                    },
                    {
                      "AgeGroup": "25_29",
                      "MalePop": 9498.5313262147,
                      "FemalePop": 9425.4454433038,
                      "TotalPop": 18923.9767695185
                    },
                    {
                      "AgeGroup": "30_34",
                      "MalePop": 7350.12472447202,
                      "FemalePop": 7293.56965072598,
                      "TotalPop": 14643.694375198
                    },
                    {
                      "AgeGroup": "35_39",
                      "MalePop": 5664.54829258414,
                      "FemalePop": 5620.96273318936,
                      "TotalPop": 11285.5110257735
                    },
                    {
                      "AgeGroup": "40_44",
                      "MalePop": 4298.06469880391,
                      "FemalePop": 4264.99340555866,
                      "TotalPop": 8563.05810436257
                    },
                    {
                      "AgeGroup": "45_49",
                      "MalePop": 3308.72086022462,
                      "FemalePop": 3283.262087482,
                      "TotalPop": 6591.98294770662
                    },
                    {
                      "AgeGroup": "50_54",
                      "MalePop": 2577.45271903127,
                      "FemalePop": 2557.62069179214,
                      "TotalPop": 5135.07341082341
                    },
                    {
                      "AgeGroup": "55_59",
                      "MalePop": 1924.14471224534,
                      "FemalePop": 1909.3395261342,
                      "TotalPop": 3833.48423837954
                    },
                    {
                      "AgeGroup": "60_64",
                      "MalePop": 1403.53807325369,
                      "FemalePop": 1392.73862155275,
                      "TotalPop": 2796.27669480644
                    },
                    {
                      "AgeGroup": "65_69",
                      "MalePop": 1055.97295394956,
                      "FemalePop": 1047.84775503259,
                      "TotalPop": 2103.82070898216
                    },
                    {
                      "AgeGroup": "70_74",
                      "MalePop": 805.312037524755,
                      "FemalePop": 799.115661784879,
                      "TotalPop": 1604.42769930963
                    },
                    {
                      "AgeGroup": "75_79",
                      "MalePop": 570.221011313828,
                      "FemalePop": 565.833511355369,
                      "TotalPop": 1136.0545226692
                    },
                    {
                      "AgeGroup": "80plus",
                      "MalePop": 398.427549070506,
                      "FemalePop": 395.361966437286,
                      "TotalPop": 793.789515507791
                    }
                  ]
                }
              ],
            }
            {status_code: 200}
        ```

        #### ERROR RESPONSE:
        ```json
            no content
            {status_code: 404}
        ```
        #### Parse sequence
        each inner polygon are calculated then executes ST_UnaryUnion(ST_MakeValid()) for initial multipolygon
        for data retrieving
        """
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Remove Geopolygon by pk

        ####**Allowed Methods**:
        ###### - DELETE

        #### **DELETE**:
        ###### URL: **api/geodata/geopolygons/{geopolygon_id}/**

        #### SUCCESS RESPONSE:
        ```json
        no content
        {status_code: 204}
        ```
        """
        instance = self.get_object()
        #TODO remove from bitmex
        result = super().destroy(request, *args, **kwargs)
        return result

    def perform_create(self, serializer):
        serializer.save(account=self.account)

    def create(self, request, *args, **kwargs):
        """
        **Save Polygon in db with parsing if multipolygon**
        ####**Allowed Methods**:
        ###### - POST

        #### **POST**:
        ###### URL: **api/geodata/geopolygons/create/**

        #### **the_geom example WKT**:
        ###### POLYGON ((21 21, 25 30, 35 30, 20 45, 21 21))
        ###### MULTIPOLYGON (((145.8142788529295 -41.3996724557645, .......)))

        #### POST DATA:
        ```json
           {
             "name": "string",
             "the_geom": "str" in WKT,
             "target_group": "int",
           }
           ```
        #### SUCCESS RESPONSE:
        ```json
               {
               "results": [
                   {
                       "id": 210,
                       "name": "Checker",
                       "geometry": "SRID=4326;MULTIPOLYGON (((145.8142788529295 -41.39967245147.3......)))",
                       "polygon": "MULTIPOLYGON (((145.8142788529295 -41.3996724557645, 145.4566......)))",
                       "target_group": 1,
                       "population_datas": [
                           {
                               "female": 51115.9695062836,
                               "male": 49435.8737201664,
                               "sum": 101638.0,
                               "mean": 16.5588139459107,
                               "max": 2234.0,
                               "min": 0.0,
                               "growth_rate": 0.395,
                               "hh_size": 1.995,
                               "Pyramids": [
                                   {
                                       "TotalPop": 4643.60747942839,
                                       "FemalePop": 2258.21509865867,
                                       "AgeGroup": "0_4",
                                       "MalePop": 2385.39238076972
                                   },
                                   {
                                       "TotalPop": 6083.8406755644,
                                       "FemalePop": 2956.4396798232,
                                       "AgeGroup": "5_9",
                                       "MalePop": 3127.4009957412
                                   },
                                   {
                                       "TotalPop": 6503.0297143288,
                                       "FemalePop": 3175.0305139908,
                                       "AgeGroup": "10_14",
                                       "MalePop": 3327.999200338
                                   },
                                   {
                                       "TotalPop": 6671.584079786,
                                       "FemalePop": 3244.5714571944,
                                       "AgeGroup": "15_19",
                                       "MalePop": 3427.0126225916
                                   },
                                   {
                                       "TotalPop": 6296.4259845708,
                                       "FemalePop": 3094.8939312528,
                                       "AgeGroup": "20_24",
                                       "MalePop": 3201.532053318
                                   },
                                   {
                                       "TotalPop": 5896.8099852944,
                                       "FemalePop": 2980.9594407712,
                                       "AgeGroup": "25_29",
                                       "MalePop": 2915.8505445232
                                   },
                                   {
                                       "TotalPop": 5659.0676044248,
                                       "FemalePop": 2923.228914478,
                                       "AgeGroup": "30_34",
                                       "MalePop": 2735.8386899468
                                   },
                                   {
                                       "TotalPop": 6075.689328292,
                                       "FemalePop": 3163.7700602984,
                                       "AgeGroup": "35_39",
                                       "MalePop": 2911.9192679936
                                   },
                                   {
                                       "TotalPop": 6710.1422642424,
                                       "FemalePop": 3487.6732504592,
                                       "AgeGroup": "40_44",
                                       "MalePop": 3222.4690137832
                                   },
                                   {
                                       "TotalPop": 7082.4522594216,
                                       "FemalePop": 3645.4184959268,
                                       "AgeGroup": "45_49",
                                       "MalePop": 3437.0337634948
                                   },
                                   {
                                       "TotalPop": 7375.3890748808,
                                       "FemalePop": 3789.2359203576,
                                       "AgeGroup": "50_54",
                                       "MalePop": 3586.1531545232
                                   },
                                   {
                                       "TotalPop": 7162.3755039976,
                                       "FemalePop": 3663.5731364696,
                                       "AgeGroup": "55_59",
                                       "MalePop": 3498.802367528
                                   },
                                   {
                                       "TotalPop": 6836.1988953804,
                                       "FemalePop": 3461.5162842796,
                                       "AgeGroup": "60_64",
                                       "MalePop": 3374.6826111008
                                   },
                                   {
                                       "TotalPop": 5752.770969696,
                                       "FemalePop": 2895.0448800264,
                                       "AgeGroup": "65_69",
                                       "MalePop": 2857.7260896696
                                   },
                                   {
                                       "TotalPop": 4484.4560414548,
                                       "FemalePop": 2278.401970816,
                                       "AgeGroup": "70_74",
                                       "MalePop": 2206.0540706388
                                   },
                                   {
                                       "TotalPop": 3391.6718296804,
                                       "FemalePop": 1787.5038267044,
                                       "AgeGroup": "75_79",
                                       "MalePop": 1604.168002976
                                   },
                                   {
                                       "TotalPop": 3926.331535986,
                                       "FemalePop": 2310.492644746,
                                       "AgeGroup": "80plus",
                                       "MalePop": 1615.83889124
                                   }
                               ]
                           }
                       ],
                   },
                   .....
               ]
           }
           <*status code:* 201>
        ```
        #### Initial polygons
        ###### name without '_i' in the end of name is the initial multipolygon
        ###### '_i' - consistent part of multipolygon. i starts from 1 to number of polygons inside

        #### NON-FIELD ERROR RESPONSE:
        ```json
           {
           "non_field_errors": [
               'There is something wrong with the_geom creation. Check documentation for geom type creation'
               'MultiPolygon and Polygon only. Check documentations',
               "Out of memory",
               ]
           }
        < *status code: *400 >
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            message = str(e) if str(e) else 'Something went wrong with multiple geometry creation.'
            return Response(
                {'non_field_errors': [message]},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
