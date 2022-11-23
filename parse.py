import re
import aiohttp
from loguru import logger
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List, Dict


@logger.catch
async def scrap_about() -> List:
    """Функция для получения информации о компании"""
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    async with aiohttp.ClientSession() as session:
        url = 'https://danielmalaev.ru/o-kompanii'
        async with session.get(url=url, headers=headers) as response:
            if response.status == 200:
                logger.info('получение информации о компании')
                result = await response.text()
                soup = BeautifulSoup(result, "lxml")
                div = soup.find('div', class_='sppb-addon-content')
                text = [re.sub('<.*?>', ' ', str(i)) for i in div]

                return text

            else:
                logger.error('Не удалось получить информацию о компании')


@logger.catch
async def scrap_delivery() -> List:
    """Функция для получения информации о оплате и доставке"""
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    async with aiohttp.ClientSession() as session:
        url = 'https://danielmalaev.ru/oplata-i-dostavka'
        async with session.get(url=url, headers=headers) as response:
            if response.status == 200:
                logger.info('получение информации о оплате и доставке')
                result = await response.text()
                soup = BeautifulSoup(result, 'lxml')
                meth = soup.findAll('div', class_='sppb-row')
                all_text = []
                for i in meth:
                    if i is not None:
                        title = i.find('div', class_='sppb-addon sppb-addon-header sppb-text-center')
                        txt_one = i.find_all('div', class_='sppb-col-md-6')[0]
                        txt_two = i.find_all('div', class_='sppb-col-md-6')[1]
                        text = '<b>' + f'{title.text}' + '</b>' + '\n' + txt_one.text + '\n\n' + txt_two.text + '\n\n'
                        all_text.append(text)

                return all_text

            else:
                logger.error('Не удалось получить информацию о оплате и доставке')


@logger.catch
async def scrap_contacts() -> List:
    """Функция для получения контактов и адресе"""
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    async with aiohttp.ClientSession() as session:
        url = 'https://danielmalaev.ru/kontakty'
        async with session.get(url=url, headers=headers) as response:
            if response.status == 200:
                logger.info('получение информации о контактах и адресе магазина')
                result = await response.text()
                soup = BeautifulSoup(result, 'lxml')
                div = soup.find_all('div', class_='sppb-addon-content')
                res = [i.text for i in div]
                contacts = str(res[0]).split('\n')

                return contacts

            else:
                logger.error('Не удалось получить информацию о контактах и адресе магазина')


@logger.catch
async def scrap_collection() -> List:
    """Функция для получения ювелирных коллекций"""
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    async with aiohttp.ClientSession() as session:
        url = 'https://danielmalaev.ru/'
        async with session.get(url=url, headers=headers) as response:
            if response.status == 200:
                logger.info('получение информации о ювелирных коллекциях')
                result = await response.text()
                soup = BeautifulSoup(result, 'lxml')
                div = soup.find_all('ul', class_="nav menu upmenu")
                for data in div:
                    li = data.find_all('li')
                res = [i.text for i in li]

                return res

            else:
                logger.error('Не удалось получить информацию о ювелирных коллекциях')


@logger.catch
async def scrap_category(collection) -> Dict:
    """Функция для получения категорий украшений"""
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    async with aiohttp.ClientSession() as session:
        url = 'https://danielmalaev.ru/' + str(collection)
        async with session.get(url=url, headers=headers) as response:
            if response.status == 200:
                logger.info('получение информации о категориях украшений')
                result = await response.text()
                soup = BeautifulSoup(result, 'lxml')
                div = soup.find_all('div', class_="category-image card")
                category = {}
                for type_jewellery in div:
                    category[type_jewellery.a['title']] = type_jewellery.a['href']

                return category

            else:
                logger.error('Не удалось получить информацию о категориях украшений')


@logger.catch
async def scrap_links(jewellery) -> List:
    """Функция для получения ссылок на украшения"""
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    async with aiohttp.ClientSession() as session:
        url = 'https://danielmalaev.ru/' + str(jewellery)
        async with session.get(url=url, headers=headers) as response:
            if response.status == 200:
                logger.info('получение ссылок на украшения')
                result = await response.text()
                soup = BeautifulSoup(result, 'lxml')
                div = soup.find_all('div', class_='flyblok')
                links = [i.a['href'] for i in div]
                return links

            else:
                logger.error('Не удалось получить ссылки на украшения')


@logger.catch
async def all_items(links) -> List:
    """Функция для получения информации из карточек товаров """
    try:
        info_list = []
        for link in links:
            ua = UserAgent()
            headers = {'User-Agent': ua.random}
            async with aiohttp.ClientSession() as session:
                url = 'https://danielmalaev.ru/' + str(link)
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        logger.info(f'получение информации из карточки товара {url}')
                        result = await response.text()
                        soup = BeautifulSoup(result, 'lxml')
                        info = dict()
                        try:
                            info['img'] = soup.find('div', class_='vmzoomer-image').a['href']
                            info['title'] = soup.find('h1', class_='b1c-name').text
                            info['price'] = soup.find('span', class_='PricesalesPrice').text
                            info['availability'] = soup.find('div', class_='nostock text-success').text
                            div = soup.find('div', class_='product-description')
                            text = [re.sub('<.*?>', '\n', str(i)) for i in div]
                            description = ''
                            for i in text:
                                description += i
                            info['description'] = description
                            info['url'] = url

                        except AttributeError:
                            info = {}

                        finally:
                            info_list.append(info)
                    else:
                        logger.error('Не удалось получить информацию из карточки товара')

        return info_list

    except Exception as ex:
        logger.exception(ex)
