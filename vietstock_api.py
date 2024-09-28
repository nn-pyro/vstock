from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from datetime import datetime
import requests


@tool
def get_time():
    """Lấy thời gian"""
    return datetime.now()


@tool
def foreign_history(code: str, from_date: str, to_date: str) -> str:

    """
        Tra cứu dữ liệu giao dịch nước ngoài từ API Vietstock.
        Xử lý các câu hỏi có liên quan đến giao dịch nước ngoài, ví dụ:
            Giao dịch nước ngoài của VNM trong năm 2024
            Dữ liệu giao dịch nước ngoài của VNM trong năm 2024
            Dữ liệu giao dịch nước ngoài hôm qua?
            Dữ liệu giao dịch nước ngoài ngày giao dịch gần nhất?
            So sánh giao dịch nước ngoài VNM qua các năm 2022, 2023, 2024
            Dữ liệu giao dịch nước ngoài tuần rồi?
            ...


        Args:
            code (str): Mã chứng khoán cần tra cứu (ví dụ: 'VNM').
            from_date (str): Ngày bắt đầu lấy dữ liệu (định dạng 'YYYY-MM-DD').
            to_date (str): Ngày kết thúc lấy dữ liệu (định dạng 'YYYY-MM-DD').

        Returns:
        str: Dữ liệu dưới dạng Json
    """

    url = f"https://api-demo.vietstock.vn/demo/foreignhistory?code={code}&fromDate={from_date}&toDate={to_date}&page=1&pageSize=20"

    try:

        res = requests.get(url)
        res.raise_for_status()

        data = res.json()

        return str(data)

    except requests.exceptions.RequestException as e:

        return f"Đã xảy ra lỗi khi lấy dữ liệu: {e}"
                
    
@tool
def event_history(code: str) -> str:

    """
            Tra cứu thông tin lịch sử sự kiện, sự kiện cổ tức và các sự kiện khác từ API Vietstock.
            Xữ lý các câu hỏi có liên quan đến các sự kiện, ví dụ:
                VNM có chia cổ tức từ năm 2020 tới nay không?, thông tin chi tiết?
                Cổ tức chia cao nhất là bao nhiêu?
                Cổ tức tiền mặt cao nhất là bao nhiêu?
                Có chia đều hàng năm không?
                Chia cổ tức tiền mặt hay cổ phiếu thì có lợi cho nhà đầu tư hơn?
                Thông tin sự kiện gần nhất của mã này?
                ...

            Args:
                code (str): Mã chứng khoán cần tra cứu (ví dụ: 'VNM').
            Returns:
                str: Dữ liệu dưới dạng Json
    """
        
    import time
    timestamp = time.time()
    timestamp = int(timestamp)


    url = f"https://api-demo.vietstock.vn/demo/marks?symbol={code}&from=1670292000&to={timestamp}&resolution=1D"
        
    try:

        res = requests.get(url)
        res.raise_for_status()

        data = res.json()

        return str(data)
        
    except requests.exceptions.RequestException as e:

        return f"Đã xảy ra lỗi khi lấy dữ liệu: {e}"
        
                
@tool
def margin_ratio(code: str) -> str:
    """
        Kiểm tra tỉ lệ ký quỹ của mã chứng khoán từ API Vietstock.
        Xử lý các câu hỏi có liên quan đến kỹ quỹ, ví dụ:
            VNM có được ký quỹ không?
            ...

        Args:
            code (str): Mã chứng khoán cần tra cứu (ví dụ: 'VNM').

        Returns:
            str: Tỉ lệ ký quỹ dưới dạng JSON hoặc thông báo lỗi.
    """
    url = f"https://api-demo.vietstock.vn/demo/tradingstatus?code={code}&languageid=1"

    try:

        res = requests.get(url)
        res.raise_for_status()

        data = res.json()

        return data
        
    except requests.exceptions.RequestException as e:

        return f"Đã xảy ra lỗi: {e}"


@tool
def company_info(code: str, language_id: int) -> str:
    """
        Lấy thông tin công ty theo mã chứng khoán.
        Xử lý các câu hỏi có liên quan đến thông tin các công ty, ví dụ:
            tên tiếng Anh mã VNM
            VNM kinh doanh trong ngành nào, có sản phẩm gì?
            thông tin chung VNM
            giám đốc VNM là ai?
            CEO có phải cổ đông lớn không?
            nếu CEO không là cổ đông lớn thì ảnh hưởng kinh doanh không?
            ...
        
        Args:
            code (str): Mã chứng khoán (ví dụ: 'VNM').
            language_id (int): 1 = Tiếng Việt, 2 = Tiếng Anh.
        
        Returns:
            str: Thông tin công ty dưới dạng JSON hoặc thông báo lỗi.
    """
    url = f"https://api-demo.vietstock.vn/demo/companyinfo?code={code}&languageID={language_id}"

    try:

        res = requests.get(url)
        res.raise_for_status()

        return res.json()
        
    except requests.exceptions.RequestException as e:

        return f"Đã xảy ra lỗi: {e}"


@tool
def major_shareholder_info(code: str) -> str:
    """
        Tra cứu thông tin cổ đông lớn của mã chứng khoán từ API Vietstock.
        Xữ lý các câu hỏi có liên quan đến cổ đông lớn, ví dụ:
            Cổ đông lớn nhất là ai?
            Cổ đông là tổ chức hay cá nhân?
            ...
        
        Args:
            code (str): Mã chứng khoán (ví dụ: 'VNM').

        Returns:
            str: Thông tin cổ đông lớn nhất hoặc thông báo lỗi.
    """
    url = f"https://api-demo.vietstock.vn/demo/stocklaborstructure?code={code}"

    try:

        res = requests.get(url)
        res.raise_for_status()

        return res.json()
        
    except requests.exceptions.RequestException as e:
            
        return f"Đã xảy ra lỗi: {e}"


@tool
def financial_info(code: str, from_date: str, to_date: str) -> str:
    """
        Tra cứu dữ liệu tài chính của mã chứng khoán từ API Vietstock.
        Xữ lý các câu hỏi có liên quan đến tài chính:
            cho tôi các mục chỉ số tài chính của VNM gần nhất
            cho tôi các mục chỉ số tài chính của VNM 2020
            ...
        
        Args:
            code (str): Mã chứng khoán cần tra cứu (ví dụ: 'VNM').
            from_date (str): Ngày bắt đầu lấy dữ liệu (định dạng 'YYYY-MM-DD').
            to_date (str): Ngày kết thúc lấy dữ liệu (định dạng 'YYYY-MM-DD').

        Returns:
            str: Dữ liệu tài chính dưới dạng JSON hoặc thông báo lỗi.
    """
    url = f"https://api-demo.vietstock.vn/demo/financeinfo?fromDate={from_date}&toDate={to_date}&code={code}&type=BCTT&termtype=N&pageSize=4"

    try:
        res = requests.get(url)
        res.raise_for_status()

        return res.json()
        
    except requests.exceptions.RequestException as e:

        return f"Đã xảy ra lỗi: {e}"