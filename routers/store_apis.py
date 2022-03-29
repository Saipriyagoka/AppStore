# Third Party Imports
import operator
from typing import List
from fastapi import APIRouter, Request
from datetime import datetime
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import starlette.status as status

# Internal Imports
from config import settings
from utils.tax_calculation import Commodity
from schemas.commodity_schema import CommodityBase, CommodityList, ProductCreateForm

router = APIRouter()
now = datetime.utcnow()
templates = Jinja2Templates(directory="templates") # template for email verification


#-------------------------Store API Account Module-------------------------------#

@router.get("/ping")
def ping():
    return "pong"

@router.get("/")
def index():
    return RedirectResponse(url="/list_of_products", status_code=status.HTTP_302_FOUND)

@router.get('/add-to-cart')
def create_product(request: Request,):
    return templates.TemplateResponse('create_product.html', {"request": request})

@router.post("/add-to-cart")
async def create_product(request: Request,):
    form = ProductCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            # saving it to Local DB
            settings.Products.update_one(
                {'item_id': form.item_id},
                {'$set': form.product}, upsert=True)
            
            return RedirectResponse(url="/list_of_products", status_code=status.HTTP_302_FOUND)
        except Exception as ex:
            settings.app_logger.info('Exception occured in /create-a-product',ex)
    return templates.TemplateResponse("create_product.html", form.__dict__)


# Endpoint for List of Files
@router.get("/list_of_products")
async def list_of_files(request: Request):
    try:
        product_info = list(settings.Products.find({}, {'_id': 0}))

        if product_info:
            return templates.TemplateResponse('list_of_products.html', 
            {"request": request, 'products': product_info})
        else:
            html_content = """
            <html>
                <body>
                    <p> No Products Found, Please click on Add to cart to create Products</p>
                    <a href=http://localhost:7899/add-to-cart><button style="background-color: rgb(78, 180, 217); border: none; color: #fff; padding: 7px 12px; text-align: center; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 7px;">Add to Cart
                </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=200)
            #return {'message': 'No Products found', 'status': 0}

    except Exception as ex:
        settings.app_logger.info('Exception occured in list_of_products',ex)
        return {'message': settings.ERROR_MESSAGE, 'status': 0}

# Endpoint for File Delete
@router.get("/remove_from_cart")
async def delete_product(item_id: str):
    try:
        product_info = settings.Products.find_one({'item_id': item_id})
        if product_info:
            settings.Products.delete_one({'item_id': item_id})
            return RedirectResponse(url="/list_of_products")
        else:
            return {'message': 'No such file', 'status': 0}

    except Exception as ex:
        settings.app_logger.info('Exception occured in /remove_from_cart',ex)
        return {'message': settings.ERROR_MESSAGE, 'status': 0}


# Endpoint for Standard Tax Calculation
@router.post('/place_order')
async def place_order(request: Request,):
#async def place_order(commodities: List[CommodityBase]):
    try:
        commodities = list(settings.Products.find({}, {'_id': 0}))
        list_of_commodities = []
        #commodities = [each.dict() for each in commodities]
        total_amount, final_amount, discount_amount, tax_amount = 0, 0, 0, 0

        for each in commodities:
            total_amount += each.get('price', 0)

        for each in commodities:
            extra_discount = 0.05 if total_amount > 2000 else 0
            list_of_commodities.append(Commodity(each, extra_discount)())
            final_amount += each.get('applicable_price', 0)
            discount_amount += each.get('discount_amount', 0)
            tax_amount += each.get('tax_amount', 0)

        sorted_list = sorted(list_of_commodities, key = lambda x: x.get('item'))

        response = {
            'purchased_date': now,
            'list_of_products': sorted_list,
            'discount': discount_amount,
            'total_tax' : tax_amount,
            'total_amount': final_amount
        }

        return templates.TemplateResponse('order.html', 
            {"request": request, 'response': response})
        #return response

    except Exception as ex:
        print('Exception occured in /place_order',ex)
        return {"message" : ex , "status" : 0}