import httpx
from bs4 import BeautifulSoup


async def extract_url_content(url: str) -> tuple[str, str]:
    async with httpx.AsyncClient(
        timeout=15.0,
        follow_redirects=True
    ) as client:
        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove content that isn't useful as article text
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()

    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else url
    )

    content = soup.get_text(separator=" ", strip=True)

    if not content:
        raise ValueError("No readable content found on the webpage")

    return title, content
