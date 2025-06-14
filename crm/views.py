from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Marketing, PlanMapping, CampaignProduct, PaymentDetails, MarketingPlan
from .serializers import MarketingSerializer, CampaignProductSerializer, PaymentDetailsSerializer, SalesDumpSerializer, MarketingPlanSerializer



@api_view(['GET'])
def get_client(request):
    client_id = request.query_params.get('client_id')
    campaign_code = request.query_params.get('campaign_code')
    chain_code = request.query_params.get('chain_code')

    if not (client_id and campaign_code and chain_code):
        return Response(
            {"error": "client_id, campaign_code, and chain_code are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Fetch the first matching Marketing record
    marketing_obj = Marketing.objects.filter(
        client_id=client_id,
        campaign_code=campaign_code,
        chain_code=chain_code
    ).first()

    if not marketing_obj:
        return Response(
            {"error": "No record found for the given identifiers."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Extract current plan code from chain_code (after last hyphen)
    payment_detail = PaymentDetails.objects.filter(
        client_id=client_id,
        campaign_code=campaign_code,
        chain_code=chain_code
    ).first()

    try:
        current_plan_code = chain_code.split('-')[-1]
        current_plan = PlanMapping.objects.get(code=current_plan_code)
        
        if current_plan_code == 'MM':
            days = 1
        else:
            days = 10
        # Get next plan by sequence
        next_plan = PlanMapping.objects.filter(
            sequence_no__gt=current_plan.sequence_no
        ).order_by('sequence_no').first()

        if next_plan:
            prefix = chain_code.rsplit('-', 1)[0]  # e.g., 'PLV_F1'
            next_chain_code = f"{prefix}-{next_plan.code}"
            next_plan_data = {
                "next_chain_code": next_chain_code,
                "description": next_plan.description,
                "next_date": payment_detail.purchase_date + timedelta(days)
            }
        else:
            next_plan_data = None
    except PlanMapping.DoesNotExist:
        next_plan_data = None


    # Serialize Marketing object
    serializer = MarketingSerializer(marketing_obj)
    response_data = serializer.data
    response_data['next_plan'] = next_plan_data

    # Include campaign product info
    campaign_product = CampaignProduct.objects.filter(
        campaign_code=campaign_code,
        chain_code=chain_code
    ).first()
    if campaign_product:
        product_serializer = CampaignProductSerializer(campaign_product)
        response_data['campaign_products'] = product_serializer.data
    else:
        response_data['campaign_products'] = None

    # Include payment details info
    if payment_detail:
        payment_serializer = PaymentDetailsSerializer(payment_detail)
        response_data['payment_details'] = payment_serializer.data
    else:
        response_data['payment_details'] = None

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_client_list(request):
    client_obj = Marketing.objects.all()
    client_serializer = MarketingSerializer(client_obj, many=True)

    return Response(client_serializer.data, status=status.HTTP_200_OK)



class CreateClient(APIView):
    def post(self, request):
        client_id = request.data.get('client_id')
        campaign_code = request.data.get('campaign_code')
        chain_code = request.data.get('chain_code')

        if not (client_id and campaign_code and chain_code):
            return Response(
                {"error": "client_id, campaign_code, and chain_code are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        exists = Marketing.objects.filter(
            client_id=client_id,
            campaign_code=campaign_code,
            chain_code=chain_code
        ).exists()

        if exists:
            return Response({"exists": True, "message": "Record already exists."})

        # Add data for creating a new record
        serializer = MarketingSerializer(data={
            "client_id": client_id,
            "origin": request.data.get("origin"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "address_1": request.data.get("address_1"),
            "address_2": request.data.get("address_2"),
            "city": request.data.get("city"),
            "zip": request.data.get("zip"),
            "country": request.data.get("country"),
            "campaign_code": campaign_code,
            "chain_code": chain_code
        })

        if serializer.is_valid():
            serializer.save()
            print(serializer)
            return Response({
                "exists": False,
                "message": "Record created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_chain_marketing(request):
    full_plan = request.query_params.get('plan')  
    if not full_plan or '-' not in full_plan:
        return Response({"error": "Please provide a valid plan like PLV_F1-MM"}, status=400)

    chain_name, _ = full_plan.split('-', 1) 
    print(chain_name)

    # Fetch all plans in order
    plans = PlanMapping.objects.all().order_by('sequence_no')

    # Build dynamic marketing fields
    result = {
        "Chain name": chain_name
    }

    for i, plan in enumerate(plans, start=1):
        plan_code = f"{chain_name}-{plan.code}"
        result[f"Marketing {i}"] = plan_code
        result[f"Description {i}"] = plan.description

    return Response(result)


# @api_view(['GET'])
# def get_chain_marketing(request):
#     plan = request.query_params.get('plan')
#     chain_name, _ = plan.split('-', 1) 

#     if not chain_name:
#         return Response({"error": "Please provide a 'chain_name' parameter"}, status=400)

#     plans = MarketingPlan.objects.filter(chain_name=chain_name).order_by('sequence_no')

#     if not plans.exists():
#         return Response({"error": f"No records found for chain_name '{chain_name}'"}, status=404)

#     response_data = {
#         "Chain name": chain_name
#     }

#     for i, plan in enumerate(plans, start=1):
#         response_data[f"Marketing {i}"] = plan.marketing_code
#         response_data[f"Description {i}"] = plan.description

#     return Response(response_data)


@api_view(['POST'])
def save_sales_dump(request):
    serializer = SalesDumpSerializer(data={'data': request.data})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Sales dump saved successfully", "id": serializer.data['id']}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def save_marketing_plan(request):
    data = request.data
    chain_name = data.get("Chain name")

    if not chain_name:
        return Response({"error": "Missing 'Chain name'"}, status=400)

    entries = []
    for i in range(1, 6):
        marketing = data.get(f"Marketing {i}")
        description = data.get(f"Description {i}")

        if marketing and description:
            entries.append(MarketingPlan(
                chain_name=chain_name,
                marketing_code=marketing,
                description=description,
                sequence_no=i
            ))

    if not entries:
        return Response({"error": "No valid marketing entries found"}, status=400)

    MarketingPlan.objects.bulk_create(entries)
    return Response({"message": f"{len(entries)} records saved successfully"})


@api_view(["GET"])
def get_plan_list(request):
    # Fetch all distinct chain names
    chain_names = MarketingPlan.objects.values_list('chain_name', flat=True).distinct()
    response_list = []

    for chain_name in chain_names:
        plans = MarketingPlan.objects.filter(chain_name=chain_name).order_by('sequence_no')
        
        result = {
            "Chain name": chain_name
        }

        for i, plan in enumerate(plans, start=1):
            result[f"Marketing {i}"] = plan.marketing_code
            result[f"Description {i}"] = plan.description

        response_list.append(result)

    return Response(response_list, status=status.HTTP_200_OK)