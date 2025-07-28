from fastapi import APIRouter, Response
from app.schemas.planetary_info import PlanetaryInfoRequest, PlanetaryInfoResponse, PlanetInfo
from app.services.planetary_info_service import get_planetary_info_table

from app.schemas.dasha import VimshottariDashaRequest, VimshottariDashaResponse, Mahadasha, Antardasha
from app.services.dasha_service import get_vimshottari_dashas

from app.schemas.ashtakavarga import AshtakavargaRequest, AshtakavargaResponse, PlanetRekhaRow
from app.services.ashtakavarga_service import get_ashtakavarga

from app.schemas.sarva_chart import SarvaChartRequest, SarvaChartResponse
from app.services.sarva_chart_service import get_sarva_chart_svg

from app.schemas.div_chart import DivChartRequest, DivChartSVGResponse
from app.services.div_chart_service import get_div_chart_svg

from app.schemas.transit_chart import TransitChartRequest, TransitChartSVGResponse
from app.services.transit_chart_service import get_transit_chart_svg


from app.schemas.progression_chart import ProgressionChartRequest, ProgressionChartSVGResponse
from app.services.progression_chart_service import get_progression_chart_svg

from app.schemas.ashtakootam import AshtakootamRequest, AshtakootamResponse
from app.services.ashtakootam_service import get_ashtakootam_data

from app.schemas.shadbala import ShadBalaRequest, ShadBalaResponse
from app.services.shadbala_service import get_shadbala_data

from app.schemas.panchang import PanchangRequest, PanchangResponse
from app.services.panchang_service import get_panchang_details



router = APIRouter()

@router.post("/planetary-info", response_model=PlanetaryInfoResponse)
def planetary_info_endpoint(payload: PlanetaryInfoRequest):
    result = get_planetary_info_table(payload)
    # Parse dicts to Pydantic models
    info_models = [PlanetInfo(**item) for item in result["info"]]
    return PlanetaryInfoResponse(info=info_models)


@router.post("/panchang", response_model=PanchangResponse)
def panchang_endpoint(payload: PanchangRequest):
    """
    Panchang endpoint.\n
    Telugu keys (in English), Telugu output values.
    """
    result = get_panchang_details(payload)
    return PanchangResponse(**result)


@router.post("/vimshottari-dashas", response_model=VimshottariDashaResponse)
def dasha_endpoint(payload: VimshottariDashaRequest):
    result = get_vimshottari_dashas(payload)
    dashas = []
    for mahadasha in result["dashas"]:
        antardashas = [Antardasha(**antar) for antar in mahadasha["antardashas"]]
        dashas.append(Mahadasha(
            mahadasha_lord=mahadasha["mahadasha_lord"],
            start=mahadasha["start"],
            end=mahadasha["end"],
            antardashas=antardashas
        ))
    return VimshottariDashaResponse(dashas=dashas)



@router.post("/ashtakavarga", response_model=AshtakavargaResponse)
def ashtakavarga_endpoint(payload: AshtakavargaRequest):
    result = get_ashtakavarga(payload)
    rekha_rows = [PlanetRekhaRow(**row) for row in result["rekha_table"]]
    return AshtakavargaResponse(
        rekha_table=rekha_rows,
        sarva=result["sarva"],
        labels=result["labels"]
    )


@router.post("/sarva-chart", response_model=SarvaChartResponse)
def sarva_chart_endpoint(payload: SarvaChartRequest):
    result = get_sarva_chart_svg(payload)
    return SarvaChartResponse(svg=result["svg"])


@router.post("/d1-chart", response_model=DivChartSVGResponse)
def d1_chart_endpoint(payload: DivChartRequest):
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d1-chart", response_model=DivChartSVGResponse)
def d1_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 1  # D1 chart (Rāśi)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d2-chart", response_model=DivChartSVGResponse)
def d2_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 2  # D2 chart (Hora)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d3-chart", response_model=DivChartSVGResponse)
def d3_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 3  # D3 chart (Drekkana)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d4-chart", response_model=DivChartSVGResponse)
def d4_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 4  # D4 chart (Chaturthamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d7-chart", response_model=DivChartSVGResponse)
def d7_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 7  # D7 chart (Saptamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d9-chart", response_model=DivChartSVGResponse)
def d9_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 9  # D9 chart (Navamsa)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d10-chart", response_model=DivChartSVGResponse)
def d10_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 10  # D10 chart (Dashamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d12-chart", response_model=DivChartSVGResponse)
def d12_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 12  # D12 chart (Dwadashamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d16-chart", response_model=DivChartSVGResponse)
def d16_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 16  # D16 chart (Shodashamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d20-chart", response_model=DivChartSVGResponse)
def d20_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 20  # D20 chart (Vimshamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d24-chart", response_model=DivChartSVGResponse)
def d24_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 24  # D24 chart (Chaturvimshamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d27-chart", response_model=DivChartSVGResponse)
def d27_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 27  # D27 chart (Bhamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d30-chart", response_model=DivChartSVGResponse)
def d30_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 30  # D30 chart (Trimsamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d40-chart", response_model=DivChartSVGResponse)
def d40_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 40  # D40 chart
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d45-chart", response_model=DivChartSVGResponse)
def d45_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 45  # D45 chart
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/d60-chart", response_model=DivChartSVGResponse)
def d60_chart_endpoint(payload: DivChartRequest):
    payload.varga_num = 60  # D60 chart (Shashtiamsha)
    result = get_div_chart_svg(payload)
    return DivChartSVGResponse(svg=result["svg"])

@router.post("/transit-chart", response_model=TransitChartSVGResponse)
def transit_chart_endpoint(payload: TransitChartRequest):
    result = get_transit_chart_svg(payload)
    return TransitChartSVGResponse(**result)


@router.post("/progression-chart", response_model=ProgressionChartSVGResponse)
def progression_chart_endpoint(payload: ProgressionChartRequest):
    result = get_progression_chart_svg(payload)
    return ProgressionChartSVGResponse(svg=result["svg"])

@router.post("/ashtakootam", response_model=AshtakootamResponse)
def ashtakootam_endpoint(payload: AshtakootamRequest):
    result = get_ashtakootam_data(payload)
    return AshtakootamResponse(**result)

@router.post("/shadbala", response_model=ShadBalaResponse)
def shadbala_endpoint(payload: ShadBalaRequest):
    result = get_shadbala_data(payload)
    return ShadBalaResponse(**result)

