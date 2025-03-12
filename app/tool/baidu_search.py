import asyncio
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from app.tool.base import BaseTool


class BaiduSearch(BaseTool):
    name: str = "baidu_search"
    description: str = """Perform a Baidu search using browser automation and return a list of relevant links.
Use this tool when you need to find information on Baidu, get up-to-date data, or research specific topics.
The tool returns a list of URLs that match the search query.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "(required) The search query to submit to Baidu.",
            },
            "num_results": {
                "type": "integer",
                "description": "(optional) The number of search results to return. Default is 10.",
                "default": 10,
            },
        },
        "required": ["query"],
    }

    async def execute(self, query: str, num_results: int = 10) -> List[str]:
        """
        Execute a Baidu search using browser automation and return a list of URLs.

        Args:
            query (str): The search query to submit to Baidu.
            num_results (int, optional): The number of search results to return. Default is 10.

        Returns:
            List[str]: A list of URLs matching the search query.
        """
        # 设置 ChromeDriver 的路径
        service = Service(executable_path="D:\\dev_tool\\chrome\\WebDriver\\bin\\chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 无头模式
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get("https://www.baidu.com")
            search_box = driver.find_element(By.NAME, 'wd')
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)

            # 等待搜索结果加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.t'))
            )

            # 获取搜索结果链接
            results = driver.find_elements(By.CSS_SELECTOR, 'h3.t a')
            links = [result.get_attribute('href') for result in results[:num_results]]

            return links
        except Exception as e:
            print(f"Error during search: {e}")
            return []
        finally:
            driver.quit()