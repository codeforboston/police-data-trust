from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class Disposition(BaseModel):
    disposition: str = Field(..., description="The disposition of the litigation.
")
    desceripton: Optional[str] = Field(None, description="A description of the disposition. This could include the terms of a settlement, the amount of a judgment, or other relevant information.
")
    date: str = Field(..., description="The date when this disposition was reached.
")


class BaseLitigation(BaseModel):
    case_title: Optional[str] = Field(None, description="The case title or caption for this litigation. Should contain the names of the parties involved.
")
    docket_number: Optional[str] = Field(None, description="The docket number for this litigation. This is the unique identifier for the case in the court system.
")
    court_level: Optional[str] = Field(None, description="The level of the court where this litigation is being heard. This could be a state court, federal court, or other court system.
")
    jurisdiction: Optional[str] = Field(None, description="The geographical or subject matter jurisdiction (e.g.,  Eastern District, Northern District, County name for  state courts) of the court where litigation is being heard.
")
    state: Optional[str] = Field(None, description="The state where this litigation is being heard. This should be the two-letter abbreviation for the state.
")
    description: Optional[str] = Field(None, description="A description of the litigation. This could include a summary of the case, the legal issues involved, or other relevant information.
")
    start_date: Optional[str] = Field(None, description="The date when this litigation was filed or initiated.
")
    dispositions: Optional[List[Disposition]] = Field(None, description="A list of any dispositions in this litigation. This could include a settlement, judgment, or other outcome.
")
    settlement_amount: Optional[float] = Field(None, description="The amount of any settlement or judgment in this litigation. This should be in USD.
")
    url: Optional[str] = Field(None, description="A URL to more information about this litigation. This could be a link to a court website such as [Court Listener](https://www.courtlistener.com/), [PACER](https://www.pacer.gov/), or other legal research resources.
")


class CreateLitigation(BaseLitigation, BaseModel):
    case_title: Optional[str] = Field(None, description="The case title or caption for this litigation. Should contain the names of the parties involved.
")
    docket_number: Optional[str] = Field(None, description="The docket number for this litigation. This is the unique identifier for the case in the court system.
")
    court_level: Optional[str] = Field(None, description="The level of the court where this litigation is being heard. This could be a state court, federal court, or other court system.
")
    jurisdiction: Optional[str] = Field(None, description="The geographical or subject matter jurisdiction (e.g.,  Eastern District, Northern District, County name for  state courts) of the court where litigation is being heard.
")
    state: Optional[str] = Field(None, description="The state where this litigation is being heard. This should be the two-letter abbreviation for the state.
")
    description: Optional[str] = Field(None, description="A description of the litigation. This could include a summary of the case, the legal issues involved, or other relevant information.
")
    start_date: Optional[str] = Field(None, description="The date when this litigation was filed or initiated.
")
    dispositions: Optional[List[Disposition]] = Field(None, description="A list of any dispositions in this litigation. This could include a settlement, judgment, or other outcome.
")
    settlement_amount: Optional[float] = Field(None, description="The amount of any settlement or judgment in this litigation. This should be in USD.
")
    url: Optional[str] = Field(None, description="A URL to more information about this litigation. This could be a link to a court website such as [Court Listener](https://www.courtlistener.com/), [PACER](https://www.pacer.gov/), or other legal research resources.
")
    defendants: Optional[List[str]] = Field(None, description="A list containing the IDs of any officers who are named as defendants in the litigation.
")


class UpdateLitigation(BaseLitigation, BaseModel):
    case_title: Optional[str] = Field(None, description="The case title or caption for this litigation. Should contain the names of the parties involved.
")
    docket_number: Optional[str] = Field(None, description="The docket number for this litigation. This is the unique identifier for the case in the court system.
")
    court_level: Optional[str] = Field(None, description="The level of the court where this litigation is being heard. This could be a state court, federal court, or other court system.
")
    jurisdiction: Optional[str] = Field(None, description="The geographical or subject matter jurisdiction (e.g.,  Eastern District, Northern District, County name for  state courts) of the court where litigation is being heard.
")
    state: Optional[str] = Field(None, description="The state where this litigation is being heard. This should be the two-letter abbreviation for the state.
")
    description: Optional[str] = Field(None, description="A description of the litigation. This could include a summary of the case, the legal issues involved, or other relevant information.
")
    start_date: Optional[str] = Field(None, description="The date when this litigation was filed or initiated.
")
    dispositions: Optional[List[Disposition]] = Field(None, description="A list of any dispositions in this litigation. This could include a settlement, judgment, or other outcome.
")
    settlement_amount: Optional[float] = Field(None, description="The amount of any settlement or judgment in this litigation. This should be in USD.
")
    url: Optional[str] = Field(None, description="A URL to more information about this litigation. This could be a link to a court website such as [Court Listener](https://www.courtlistener.com/), [PACER](https://www.pacer.gov/), or other legal research resources.
")
    defendants: Optional[List[str]] = Field(None, description="A list containing the IDs of any officers who are named as defendants in the litigation.
")


class Litigation(BaseLitigation, BaseModel):
    case_title: str = Field(..., description="The case title or caption for this litigation. Should contain the names of the parties involved.
")
    docket_number: str = Field(..., description="The docket number for this litigation. This is the unique identifier for the case in the court system.
")
    court_level: str = Field(..., description="The level of the court where this litigation is being heard. This could be a state court, federal court, or other court system.
")
    jurisdiction: str = Field(..., description="The geographical or subject matter jurisdiction (e.g.,  Eastern District, Northern District, County name for  state courts) of the court where litigation is being heard.
")
    state: str = Field(..., description="The state where this litigation is being heard. This should be the two-letter abbreviation for the state.
")
    description: Optional[str] = Field(None, description="A description of the litigation. This could include a summary of the case, the legal issues involved, or other relevant information.
")
    start_date: Optional[str] = Field(None, description="The date when this litigation was filed or initiated.
")
    dispositions: Optional[List[Disposition]] = Field(None, description="A list of any dispositions in this litigation. This could include a settlement, judgment, or other outcome.
")
    settlement_amount: Optional[float] = Field(None, description="The amount of any settlement or judgment in this litigation. This should be in USD.
")
    url: Optional[str] = Field(None, description="A URL to more information about this litigation. This could be a link to a court website such as [Court Listener](https://www.courtlistener.com/), [PACER](https://www.pacer.gov/), or other legal research resources.
")
    uid: Optional[str] = Field(None, description="The uid of the litigation")
    documents: Optional[str] = Field(None, description="A link to retrieve the documents associated with this litigation")
    defendants: List[Officer] = Field(..., description="A list of any officers who are named as defendants in the litigation.
")


class LitigationList(PaginatedResponse, BaseModel):
    results: Optional[List[Litigation]] = None


class BaseDocument(BaseModel):
    title: Optional[str] = Field(None, description="The title of the document")
    description: Optional[str] = Field(None, description="A description of the document")
    url: Optional[str] = Field(None, description="A URL to the document")


class CreateDocument(BaseDocument, BaseModel):
    title: Optional[str] = Field(None, description="The title of the document")
    description: Optional[str] = Field(None, description="A description of the document")
    url: Optional[str] = Field(None, description="A URL to the document")


class Document(BaseDocument, BaseModel):
    title: Optional[str] = Field(None, description="The title of the document")
    description: Optional[str] = Field(None, description="A description of the document")
    url: Optional[str] = Field(None, description="A URL to the document")
    uid: Optional[str] = Field(None, description="The uid of the document")


class DocumentList(PaginatedResponse, BaseModel):
    results: Optional[List[Document]] = None


