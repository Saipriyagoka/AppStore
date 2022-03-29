

from fastapi import Header, HTTPException, status
from schemas.commodity_schema import CommodityList

def validate_request(commodities: CommodityList, content_type: str = Header(...)):
    if content_type != "application/json":
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Unsupported media type: {content_type}."
            " It must be application/json",
        )

    
