import random
import time
from playwright.sync_api import sync_playwright

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    # 其他 User-Agent
]

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=random.choice(user_agents))

        # 手动添加有效的 Cookies
        context.add_cookies([{
            'name': 'cookie_name',
            'value': 'cookie_value',
            'domain': '.sunsetbot.top',  # 使用正确的域名
            'path': '/'                   # 使用根路径
        }])

        page = context.new_page()

        try:
            page.goto("https://sunsetbot.top/")
            print("当前页面URL:", page.url)
            page.wait_for_load_state("networkidle")  # 等待网络空闲
            time.sleep(random.uniform(2, 5))  # 随机延迟

            if "404" in page.url:
                print("页面未找到（404）。请检查 URL。")
            else:
                print("页面加载完成，当前URL:", page.url)

                # 模拟输入城市
                city_input = page.wait_for_selector("#city_input")
                city_input.fill("上海")
                time.sleep(random.uniform(1, 3))

                # 模拟选择事件
                event_selector = page.wait_for_selector("#event_selector")
                event_selector.fill("今天日落")
                time.sleep(random.uniform(1, 3))

                # 点击搜索按钮
                srch_btn = page.wait_for_selector("#srch_btn")
                srch_btn.click()
                time.sleep(5)  # 等待数据加载

                # 获取数据
                table = page.wait_for_selector("#xsection_fcst_tbody")
                rows = table.query_selector_all("tr")

                for row in rows:
                    cells = row.query_selector_all("td")
                    if len(cells) > 0:
                        event_time = cells[0].inner_text().strip()
                        quality = cells[1].inner_text().strip()
                        aod = cells[2].inner_text().strip()
                        uncertainty = cells[3].inner_text().strip()

                        print(f"Event Time: {event_time}")
                        print(f"Quality: {quality}")
                        print(f"AOD: {aod}")
                        print(f"Uncertainty: {uncertainty}")
                        print("-" * 40)

        except Exception as e:
            print("发生错误:", e)

        finally:
            browser.close()

if __name__ == "__main__":
    main()
