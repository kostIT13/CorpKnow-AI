from fastapi import APIRouter, UploadFile, File, status, HTTPException
from src.api.document.schemas import DocumentListResponse, DocumentResponse, DocumentUploadResponse
from src.api.document.dependencies import DocumentDependency, DocumentServiceDependency
from src.api.auth.dependencies import CurrentUserDependency
from typing import List

router = APIRouter(prefix='/documents', tags=["Documents"])


@router.get('/', response_model=List[DocumentListResponse])
async def get_user_documents(
    current_user: CurrentUserDependency,
    service: DocumentServiceDependency
):
    documents = await service.get_user_documents(current_user.id)
    return documents


@router.post('/upload', response_model=DocumentUploadResponse)
async def upload_document(
    current_user: CurrentUserDependency,
    service: DocumentServiceDependency,
    file: UploadFile = File(...)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Имя файла не указано")
    
    if not file.content_type:
        raise HTTPException(status_code=400, detail="Тип файла не определён")
    
    file_content = await file.read()
    
    if len(file_content) > 10 * 1024 * 1024: 
        raise HTTPException(status_code=400, detail="Файл слишком большой (макс. 10MB)")
    
    document = await service.upload_document(
        user_id=current_user.id,
        filename=file.filename,
        file_content=file_content,
        file_type=file.content_type
    )
    
    return DocumentUploadResponse(
        id=document.id,
        filename=document.filename,
        status=document.status,
        message="Документ загружен и обрабатывается",
        created_at=document.created_at
    )


@router.get('/{doc_id}', response_model=DocumentResponse)
async def get_document(document: DocumentDependency):
    return document


@router.delete('/{doc_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document: DocumentDependency,
    service: DocumentServiceDependency
):
    await service.delete_document(document.id, document.user_id)
    return None