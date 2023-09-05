"""
this file is used to scrap the news from websites,
there are a function for each website
- CoinTelegraph
- CoinPedia
- AmbCrypto
- Cryptopolitan
- The News Crypto
"""
import hashlib
import re
from time import time as t
import time

import coreapi
import requests
from bs4 import BeautifulSoup


def save_new_in_database(source, title, url, image_url, summary, category, date, content):
    # check data integrity
    if date is None:
        date = int(t())
    if content is None:
        content = ""
    if summary is None:
        summary = ""

    # Initialize a client & load the schema document
    client = coreapi.Client()
    schema = client.get("http://backend:8000/news/docs/")

    # Interact with the API endpoint
    action = ["news", "create"]
    params = {
        "id": int(hashlib.sha256(url.encode('utf-8')).hexdigest(), 16) % 10 ** 8,
        "source": source,
        "title": title,
        "url": url,
        "image_url": image_url,
        "summary": summary,
        "category": category,
        "date": date,
        "content": content
    }
    try:
        client.action(schema, action, params=params)
    except coreapi.exceptions.ErrorMessage as e:
        if "new with this id already exists." in e.error:
            pass


def get_coin_telegraph_news(tag):
    """
    This function get the news from CoinTelegraph
    :param tag: Tag to search in CoinTelegraph
    :return:
    """
    url = "https://cointelegraph.com/tags/" + tag
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 '
                                                        'Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                                                    'image/avif,image/webp,*/*;q=0.8',
                                          'Referer': 'https://cointelegraph.com',
                                          'Host': 'cointelegraph.com'})
    soup = BeautifulSoup(response.text, "html.parser")
    # All news are in li with class "posts-listing__item"
    news = soup.find_all("li", class_="posts-listing__item")
    for new in news:
        # get title on span class "post-card-inline__title"
        title = new.find("span", class_="post-card-inline__title").text
        title = re.sub(r"^\s", "", title)
        # get url on a class "post-card-inline__figure-link"
        url = "https://cointelegraph.com" + new.find("a", class_="post-card-inline__figure-link")["href"]
        try:
            image_request = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) '
                                                                     'Gecko/20100101 Firefox/110.0',
                                                       'Accept': 'text/html,application/xhtml+xml,application/'
                                                                 'xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                                                       'Referer': 'https://cointelegraph.com',
                                                       'Host': 'cointelegraph.com'})
            image_soup = BeautifulSoup(image_request.text, "html.parser")
            image_url = image_soup.find("img", class_="lazy-image__img")["src"]
        except TypeError:
            image_url = "https://s3.cointelegraph.com/storage/uploads/view/e8ede6f43a40811fcfeb9354d0a7f25b.jpg"
        # get summary on p class "post-card-inline__text"
        summary = new.find("p", class_="post-card-inline__text").text
        # expresion regular para borrar dobles espacios
        summary = re.sub(r"^\s", "", summary)
        # get category on span class "post-card-inline__badge post-card-inline__badge_default"
        try:
            category = new.find("span", class_="post-card-inline__badge post-card-inline__badge_default").text
            category = re.sub(r"^\s", "", category)
        except AttributeError:
            try:
                category = new.find("span", class_="post-card-inline__badge post-card-inline__badge_info").text
                category = re.sub(r"^\s", "", category)
            except AttributeError:
                try:
                    category = new.find("span", class_="post-card-inline__badge post-card-inline__badge_success").text
                    category = re.sub(r"^\s", "", category)
                except AttributeError:
                    try:
                        category = new.find("span", class_="post-card-inline__badge post-card-inline__badge_").text
                        category = re.sub(r"^\s", "", category)
                    except AttributeError:
                        category = "Crypto News"

        # Create news object
        # Save news in database
        save_new_in_database(source="CoinTelegraph",
                             title=title,
                             url=url,
                             image_url=image_url,
                             summary=summary,
                             category=category,
                             date=None,
                             content=None)


def get_coinpedia_news():
    """
    This function get the news from CoinPedia
    :return:
    """
    url = "https://coinpedia.org/news/"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 '
                                                        'Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                                                    'image/avif,image/webp,*/*;q=0.8'})
    soup = BeautifulSoup(response.text, "html.parser")
    # All news are in ul with class "posts-items"
    news = soup.find_all("ul", class_="posts-items")
    # divide news in li
    news = news[0].find_all("li")
    for new in news:
        # get title on h2 class "post-title"
        title = new.find("h2", class_="post-title").text
        title = re.sub(r"^\s", "", title)
        # get url on a class "post-thumb" and href
        url = new.find("a", class_="post-thumb")["href"]
        # get image url on img class "attachment-jannah-image-large size-jannah-image-large wp-post-image entered
        # lazyloaded"
        image_url = new.find("img")["data-lazy-src"]
        # get summary on p class "post-excerpt"
        summary = new.find("p", class_="post-excerpt").text
        summary = re.sub(r"^\s", "", summary)
        # get category on div class "tag_hash_display" and span
        category_aux = new.find("div", class_="tag_hash_display").find_all("span")
        category = ""
        for cat in category_aux:
            category = category + cat.text + " "
        category = re.sub(r"^\s", "", category)
        if category == "" or category == "Crypto news":
            category = "Crypto News"
        # get date on span class "date meta-item tie-icon"
        date = new.find("span", class_="date meta-item tie-icon").text
        # Create news object
        # Save news in database
        save_new_in_database(source="CoinPedia",
                             title=title,
                             url=url,
                             image_url=image_url,
                             summary=summary,
                             category=category,
                             date=None,
                             content=None)


def get_ambcrypto_news():
    """
    This function get the news from AmbCrypto
    :return:
    """
    url = "https://ambcrypto.com/category/new-news/"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 '
                                                        'Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                                                    'image/avif,image/webp,*/*;q=0.8'})
    soup = BeautifulSoup(response.text, "html.parser")
    # News are on ul class "home-posts infinite-content"
    news = soup.find_all("ul", class_="home-posts infinite-content")
    # divide news in li
    try:
        news = news[0].find_all("li")
    except IndexError:
        news = []
    for new in news:
        # get image url on img data-lazy-src
        image_url = new.find("img")["data-lazy-src"]
        # get news url on a href in div class "home-post-image"
        url = new.find("div", class_="home-post-image").find("a")["href"]
        # get title on h2 into div class "home-post-content"
        title = new.find("div", class_="home-post-content").find("h2").text
        # get category on a class "mvp-cd-cat left relative"
        category = new.find("a", class_="mvp-cd-cat left relative").text
        summary = None
        # Create news object
        # Save news in database
        save_new_in_database(source="AmbCrypto",
                             title=title,
                             url=url,
                             image_url=image_url,
                             summary=summary,
                             category=category,
                             date=None,
                             content=None)


def get_cryptopolitan_news(url):
    """
    This function get the news from Cryptopolitan
    :param url: Url to get news from different categories from Cryptopolitan
    :return:
    """
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) '
                                                        'Gecko/20100101 Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/'
                                                    'xml;q=0.9,image/avif,image/webp,*/*;q=0.8'})
    soup = BeautifulSoup(response.text, "html.parser")
    # News are in article
    news = soup.find_all("article")
    for new in news:
        # get image on img class "grid-image ls-is-cached lazyloaded"
        try:
            image_url = new.find("img")["data-src"]
        except Exception:
            image_url = None
        # get url on a class "grid-image-holder"
        try:
            url = new.find("a", class_="grid-image-holder")["href"]
        except TypeError:
            url = None
        # get title on h3 class "cp-post-title"
        try:
            title = new.find("h3", class_="cp-post-title").text
            title = re.sub(r"^\s", "", title)
            title = re.sub(r"^\n", "", title)
        except TypeError:
            title = None
        # get summary on p class "cp-excerpt"
        try:
            summary = new.find("p", class_="cp-excerpt").text
        except:
            summary = None
        # get category on div class "cat-container"
        try:
            category = new.find("div", class_="cat-container").text
        except:
            category = None
        # get date on first span into div class "cp-post-meta"
        try:
            date = new.find("div", class_="cp-post-meta").find("span").text
        except TypeError:
            date = None
        if url is not None and title is not None:
            # Save news in database
            save_new_in_database(source="Cryptopolitan",
                                 title=title,
                                 url=url,
                                 image_url=image_url,
                                 summary=summary,
                                 category=category,
                                 date=None,
                                 content=None)


def get_thenewscrypto_news(tag):
    url = f"https://thenewscrypto.com/{tag}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) '
                                                        'Gecko/20100101 Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/'
                                                    'xml;q=0.9,image/avif,image/webp,*/*;q=0.8'})
    soup = BeautifulSoup(response.text, "html.parser")
    # news are in div class "card mb-3 shadow-sm text-box"
    news = soup.find_all("div", class_="card mb-3 shadow-sm text-box")
    for new in news:
        # get image on img class in a class "h-100 w-100 d-inline-block" src
        image_url = new.find("img")["data-lazy-src"]
        # get url on a class "h-100 w-100 d-inline-block" href
        url = new.find("a", class_="h-100 w-100 d-inline-block")["href"]
        # get title on a class "text-decoration-none text-dark" text
        title = new.find("a", class_="text-decoration-none text-dark").text
        # get summary on p into div class "d-flex flex-column justify-content-around h-100"
        summary = new.find("div", class_="d-flex flex-column justify-content-around h-100").find("p").text
        # get category based on tag
        category = tag
        category = re.sub(r"-", " ", category)
        category = re.sub(r"/", " ", category)
        category = re.sub(r"^\s", "", category)
        category = re.sub(r"^\n", "", category)
        category = category.title()
        category = re.sub(r"News", "", category)
        category = category.title()

        # create news object
        # Save news in database
        save_new_in_database(source="The News Crypto",
                             title=title,
                             url=url,
                             image_url=image_url,
                             summary=summary,
                             category=category,
                             date=None,
                             content=None)


def get_newsbtc_news(tag):
    url = f"https://www.newsbtc.com/{tag}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) '
                                                        'Gecko/20100101 Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/'
                                                    'xml;q=0.9,image/avif,image/webp,*/*;q=0.8'})
    soup = BeautifulSoup(response.text, "html.parser")
    # News are in div class "jeg_posts jeg_load_more_flag"
    news = soup.find_all("div", class_="jeg_posts jeg_load_more_flag")
    # divide news in article
    try:
        news = news[0].find_all("article")
    except IndexError:
        news = []
    for new in news:
        # get image on img into div class "thumbnail-container animate-lazy  size-715" src
        try:
            image_url = new.find("img")["data-src"]
        except TypeError:
            image_url = None
        # get url on a href in h3 class "jeg_post_title"
        url = new.find("h3", class_="jeg_post_title").find("a")["href"]
        # get title on a href in h3 class "jeg_post_title"
        title = new.find("h3", class_="jeg_post_title").find("a").text
        # get summary on p class "jeg_post_excerpt"
        summary = new.find("div", class_="jeg_post_excerpt").find("p").text
        # get category from tag
        category = tag
        category = re.sub(r"/", " ", category)
        category = re.sub(r"^\s", "", category)
        category = re.sub(r"^\n", "", category)
        category = category.title()
        if 'News' in category:
            category = re.sub(r"News ", "", category)
        if 'Defi' in category:
            category = 'DeFi'
        if category == '':
            category = "News"
        # create news object
        # Save news in database
        save_new_in_database(source="NewsBTC",
                             title=title,
                             url=url,
                             image_url=image_url,
                             summary=summary,
                             category=category,
                             date=None,
                             content=None)


def get_thecryptobasic_news(tag):
    url = f"https://thecryptobasic.com/{tag}"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) '
                                                            'Gecko/20100101 Firefox/110.0',
                                              'Accept': 'text/html,application/xhtml+xml,application/'
                                                        'xml;q=0.9,image/avif,image/webp,*/*;q=0.8'})
        soup = BeautifulSoup(response.text, "html.parser")
        # News are in div class "tdb_module_loop td_module_wrap td-animation-stack td-cpt-post"
        news = soup.find_all("div", class_="tdb_module_loop td_module_wrap td-animation-stack td-cpt-post")
        for new in news:
            # Get image on span class "entry-thumb td-thumb-css rocket-lazyload entered lazyloaded"
            image_url = new.find("span", class_="entry-thumb td-thumb-css rocket-lazyload")["data-bg"]
            # get url on a class "td-image-wrap" href
            url = new.find("a", class_="td-image-wrap")["href"]
            # get title on h3 class "entry-title td-module-title"
            title = new.find("h3", class_="entry-title td-module-title").find("a").text
            # get summary on div class "td-excerpt"
            summary = new.find("div", class_="td-excerpt").text
            summary = re.sub(r"^\n", "", summary)

            # get date on time class "entry-date updated td-module-date" text
            date = new.find("time", class_="entry-date updated td-module-date").text
            # get category from tag
            category = tag
            category = re.sub(r"/", " ", category)
            category = re.sub(r"-", " ", category)
            category = re.sub(r"^\s", "", category)
            category = re.sub(r"^\n", "", category)
            category = category.title()
            # expresion regular para eliminar las palabras "News" y "Tag" de la categoria
            category = re.sub(r"News", "", category)
            category = re.sub(r"Tag", "", category)
            category = re.sub(r"Category", "", category)
            # eliminar los espacios del principio y final de la categoria
            category = re.sub(r"^\s", "", category)
            # eliminar el espacio del final de la categoria
            category = re.sub(r"\s$", "", category)
            category = category.title()

            # create news object
            # Save news in database
            save_new_in_database(source="The Crypto Basic",
                                 title=title,
                                 url=url,
                                 image_url=image_url,
                                 summary=summary,
                                 category=category,
                                 date=None,
                                 content=None)
    except Exception as e:
        print(e)
        pass

def get_livebitcoinnews_news(tag):
    url = f"https://www.livebitcoinnews.com/{tag}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) '
                                                        'Gecko/20100101 Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/'
                                                    'xml;q=0.9,image/avif,image/webp,*/*;q=0.8'})
    soup = BeautifulSoup(response.text, "html.parser")
    # News are into div class "jeg_posts jeg_load_more_flag" in article class "jeg_post jeg_pl_lg_2 format-standard"
    news = soup.find_all("div", class_="jeg_posts jeg_load_more_flag")
    # divide news in article
    try:
        news = news[0].find_all("article")
    except IndexError:
        news = []
    for new in news:
        image_url = new.find("img")["data-src"]
        url = new.find("a")["href"]
        # title on h3 class "jeg_post_title"
        title = new.find("h3", class_="jeg_post_title").find("a").text
        # no summary
        summary = None
        # get date on span class "jeg_meta_date"
        date = new.find("div", class_="jeg_meta_date").text
        # remove the first space
        date = re.sub(r"^\s", "", date)
        # get category from class "jeg_meta_category"
        category = new.find("div", class_="jeg_post_category").find("a").text
        # create news object
        # Save news in database
        save_new_in_database(source="Live Bitcoin News",
                             title=title,
                             url=url,
                             image_url=image_url,
                             summary=summary,
                             category=category,
                             date=None,
                             content=None)


def get_cryptonews(page):
    url = f"https://cryptonews.com/news/{page}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:110.0) '
                                                        'Gecko/20100101 Firefox/110.0',
                                          'Accept': 'text/html,application/xhtml+xml,application/'
                                                    'xml;q=0.9,image/avif,image/webp,*/*;q=0.8'})

    soup = BeautifulSoup(response.text, "html.parser")
    # get all article class mb-15 mb-sm-30 article-item
    news = soup.find_all("article", class_="mb-15 mb-sm-30 article-item")
    for new in news:
        try:
            # get summary on div class mb-25 d-none d-md-block into div class class="col-12 col-md-7 column-45__right d-flex flex-column justify-content-center"
            summary = new.find("div", class_="mb-25 d-none d-md-block").text
            # get title on a class article__title article__title--lg article__title--featured mb-20
            title = new.find("a", class_="article__title article__title--lg article__title--featured mb-20").text
            # get image url on img class img-fluid src
            image_url = new.find("img", class_="img-fluid")["src"]
            # get url on href in a <a class="article__title article__title--lg article__title--featured mb-20"
            article_url = new.find("a", class_="article__title article__title--lg article__title--featured mb-20")["href"]
            # get categoty on article__badge article__badge--md a class
            category = new.find("a", class_="article__badge article__badge--md").text
            category = re.sub(r" News", "", category)
            category = re.sub(r"^\s", "", category)

            save_new_in_database(source="Crypto News",
                                 title=title,
                                 url=article_url,
                                 image_url=image_url,
                                 summary=summary,
                                 category=category,
                                 date=None,
                                 content=None)
        except Exception:
            pass


if __name__ == '__main__':
    while True:
        get_cryptonews("")
        get_cryptonews("bitcoin-news")
        get_cryptonews("blockchain-news")
        get_cryptonews("ethereum-news")
        get_cryptonews("defi-news")
        get_cryptonews("finance-news")
        get_cryptonews("ico-news")
        get_cryptonews("technology-news")
        get_cryptonews("industry-talk")
        get_cryptonews("cryptonews-deals")
        get_cryptonews("press-releases")
        get_cryptonews("altcoin-news")

        get_livebitcoinnews_news("news/bitcoin-news/")
        get_livebitcoinnews_news("news/altcoin-news/")
        get_livebitcoinnews_news("news/exchange-news/")
        get_livebitcoinnews_news("news/dogecoin-news/")

        get_thecryptobasic_news("category/latest-crypto-news/")
        get_thecryptobasic_news("tag/bitcoin/")
        get_thecryptobasic_news("tag/ethereum/")
        get_thecryptobasic_news("tag/ripple/")
        get_thecryptobasic_news("tag/cardano/")
        get_thecryptobasic_news("tag/shiba-inu/")
        get_thecryptobasic_news("tag/altcoins/")
        get_thecryptobasic_news("tag/crypto-exchanges/")
        get_thecryptobasic_news("category/cryptocurrency-trading-bot/")
        get_thecryptobasic_news("category/cryptocurrency-guides/")
        get_thecryptobasic_news("category/cryptocurrency-exchanges/")

        get_newsbtc_news("news/")
        get_newsbtc_news("news/bitcoin/")
        get_newsbtc_news("news/ethereum/")
        get_newsbtc_news("news/cardano/")
        get_newsbtc_news("news/dogecoin/")
        get_newsbtc_news("news/ripple/")
        get_newsbtc_news("news/defi/")
        get_newsbtc_news("nft/")
        get_newsbtc_news("analysis/btc/")
        get_newsbtc_news("analysis/eth/")
        get_newsbtc_news("analysis/ada/")
        get_newsbtc_news("analysis/link/")
        get_newsbtc_news("analysis/ltc/")
        get_newsbtc_news("analysis/xtz/")
        get_newsbtc_news("analysis/zec/")
        get_newsbtc_news("analysis/eos-price/")
        get_newsbtc_news("news/yearnfinance/")

        get_thenewscrypto_news("altcoin-news")
        get_thenewscrypto_news("bitcoin-news")
        get_thenewscrypto_news("news/ethereum-news/")
        get_thenewscrypto_news("blockchain-news/")
        get_thenewscrypto_news("news/nft-news/")
        get_thenewscrypto_news("exchange-news/")
        get_thenewscrypto_news("news/metaverse/")
        get_thenewscrypto_news("market-news")
        get_thenewscrypto_news("markets/price-analysis/")
        get_thenewscrypto_news("markets/price-prediction/")
        get_thenewscrypto_news("learn/")

        get_cryptopolitan_news("https://www.cryptopolitan.com/news/")
        get_cryptopolitan_news("https://www.cryptopolitan.com/price-prediction/")
        get_cryptopolitan_news("https://www.cryptopolitan.com/guides/")
        get_cryptopolitan_news("https://www.cryptopolitan.com/news/regulation/")
        get_cryptopolitan_news("https://www.cryptopolitan.com/news/research/")
        get_cryptopolitan_news("https://www.cryptopolitan.com/news/scam/")
        get_cryptopolitan_news("https://www.cryptopolitan.com/technology/")

        get_ambcrypto_news()

        get_coinpedia_news()

        get_coin_telegraph_news("bitcoin")
        get_coin_telegraph_news("ethereum")
        get_coin_telegraph_news("altcoin")
        get_coin_telegraph_news("blockchain")
        get_coin_telegraph_news("business")
        get_coin_telegraph_news("regulation")
        get_coin_telegraph_news("nft")
        get_coin_telegraph_news("defi")
        get_coin_telegraph_news("adoption")

        time.sleep(10)  # 10 seconds
