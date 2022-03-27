import base64
import math
import mimetypes
import os
import shutil
from typing import List, Any
import uuid
from fastapi import Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from pandas import DataFrame
from app.api.products.schema import DataFrameResponseType, FileResponseType, ImageB64Response, ImageLinkResponse
from app.utils.paths import OUTPUTS_DIR


def get_success_response(result: List[Any], message: str):
    return {"status": "success", "message": message, "result": result}


def get_success_response_for_query(limit: int, total: int, offset: int, result: List[Any], message: str):
    return {
        "status": "success",
        "message": message,
        "limit": limit,
        "pages": math.ceil(total/limit),
        "page": math.floor(offset/limit)+1,
        "result": result
    }


def get_error_response(message: str, result: List[Any] = None):
    return {
        "status": "error",
        "message": message,
        "result": [] if result is None else result,
    }

# Dataframe Repsonses


def get_dataframe_response(option: DataFrameResponseType, dataframe: DataFrame,):
    dataframe = dataframe.fillna('') # JSON cannot represent NaN values, so change to space
    if(option.value == DataFrameResponseType.columns.value):
        return dataframe.to_dict(orient='split')
    if(option.value == DataFrameResponseType.records.value):
        return dataframe.to_dict(orient='records')

# File Responses - Provide different methods for returning files as File objects, links to download
# or base64-encoded data


def get_file_response(option: FileResponseType, filepath: str, request: Request):
    if(option.value == FileResponseType.file.value):
        return FileResponse(filepath)
    if(option.value == FileResponseType.base64.value):
        return get_file_b64_response(filepath)
    if(option.value == FileResponseType.link.value):
        return get_file_link_response(filepath, request)


def get_file_b64_response(filepath: str):
    with open(filepath, 'rb') as f:
        base64image = base64.b64encode(f.read())
        mimetype = mimetypes.MimeTypes().guess_type(filepath)[0]
        res = ImageB64Response(mimetype=mimetype, data=base64image)
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)


def get_file_link_response(filepath: str, request: Request):
    # Generate a static file with a random name and return a json response with reference
    fileExtension = os.path.splitext(filepath)[1]
    basename = str(uuid.uuid4())
    outputname = f"{basename}{fileExtension}"
    outputPath = os.path.join(OUTPUTS_DIR, outputname)
    shutil.copy(filepath, outputPath)
    url = request.url
    link = f"{url.scheme}://{url.hostname}:{url.port}/outputs/{outputname}"
    mimetype = mimetypes.MimeTypes().guess_type(filepath)[0]
    res = ImageLinkResponse(link=link, mimetype=mimetype)
    json_compatible_item_data = jsonable_encoder(res)
    return JSONResponse(content=json_compatible_item_data)
