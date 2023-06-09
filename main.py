from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from openai_nlp import updateWithNLP
from price_parser import extractPriceWithJS
from html_requests import *

# Current testing links 
test_input_links = ['https://us.shein.com/EMERY-ROSE-Knot-Front-Pocket-Patched-Overall-Romper-Without-Tube-Top-p-10748193-cat-1860.html?src_identifier=fc%3DWomen%60sc%3DCLOTHING%60tc%3DJUMPSUITS%20%26%20BODYSUITS%60oc%3DJumpsuits%60ps%3Dtab01navbar05menu05dir01%60jc%3Dreal_1860&src_module=topcat&src_tab_page_id=page_home1685625317165&mallCode=1', 
                   'https://www.zara.com/us/en/convertible-crop-jacket-p04661815.html?v1=272715073&v2=2184220', 
                   'https://www.lulus.com/products/show-stopper-cream-embroidered-sequin-bodycon-midi-dress/856342.html',
                   'https://www.madewell.com/on/demandware.store/Sites-madewellUS-Site/en_US/Product-Multisell?externalProductCodes=NK023,NK842,NH399,NL556'
                   'https://www.macys.com/shop/product/levis-womens-726-high-rise-flare-jeans?ID=14231961&CategoryID=51475'
                   'https://www.express.com/clothing/women/stylist-super-high-waisted-pleated-pull-on-shorts/pro/03016256/color/RUM%20RAISIN/',
                   'https://www.uniqlo.com/us/en/products/E456191-000/00?colorDisplayCode=01&sizeDisplayCode=003'
                    ]


# Empty list to store the resulting HTML and product info
output_html = []
product_info_list = []
extracted_fields = {}


########### SESSION CREATION AND FUNCTION CALLS ############

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-images")  # Disable images
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)


s = Service('Users/user/Downloads/chromedriver_mac64')  # Replace with your actual path
driver = webdriver.Chrome(service=s, options=chrome_options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# Loop through all links and get the HTML content
for link in test_input_links:
    try:
        # Navigate to the page
        driver.get(link)

        # Get the page source and parse it using BeautifulSoup
        html = BeautifulSoup(driver.page_source, 'html.parser')

        extracted_fields["PRICE"] = None

        extracted_fields = extractFromTags(html)

        if extracted_fields["PRICE"] is None or extracted_fields["PRICE"] in ["0", "1"]:
            extracted_fields["PRICE"] = extractPriceWithJS(driver)

        if extracted_fields["PRICE"] is None or extracted_fields["PRICE"] in ["0", "1"]:
            if((product_info := getProductSchema(html)) is not None):
                extracted_fields.update(extractSchemaFields(product_info))


        

        print(extracted_fields["PRICE"])
        

        # output_html.append(html.prettify())

        # # Extract product info JSON string from the HTML
        # if((product_info := getProductSchema(html)) is not None):
        #     extracted_fields.append(extractSchemaFields(product_info))
        #     product_info_list.append(product_info) #For Testing

        # else:
        #     if((product_info := extractFromTags(html)) is not None):
        #         extracted_fields.append(product_info)
        #         product_info_list.append(product_info) # For Testing

        #     else:
        #         extracted_fields.append(None)
        #         product_info_list.append(None) # For Testing

    except Exception as e:
        output_html.append(None)
        print('An error occurred: ', e)

# Quit the webdriver when done
driver.quit()

######### Update with NLP ############

# # Updating extracted fields with NLP parser results
# for i, extracted_field in enumerate(extracted_fields):
#     if extracted_field is not None:
#         extracted_fields[i] = updateWithNLP(extracted_field)





########### PROGRAM OUTPUT ############

# Printing for error checking
# for i in range(len(test_input_links)):
#     if output_html[i] is None:
#          print(f'HTML content of {test_input_links[i]} was not retrieved')
#     if product_info_list[i] is None:
#          print(f'Product info of {test_input_links[i]} was not retrieved')

# # Outputting product info to json files
# for i, extracted_field in enumerate(extracted_fields):
#     with open(f'output_{i}.json', 'w') as f:
#         #json.dump(product_info, f)
#         json.dump(extracted_fields[i], f)

# # Outputting HTML to text files
# for i, html in enumerate(output_html):
#     with open(f'output_{i}.txt', 'w') as f:
#         f.write(html)



# List of links working 
all_input_links = ['https://www.nike.com/t/blazer-mid-pro-club-mens-shoes-Vgslvc/DQ7673-003', 
                   'https://www2.hm.com/en_us/productpage.1195139001.html', 
                   'https://fearofgod.com/collections/essentials/products/sp23-ss-sweatshirt-off-black', 
                   'https://www.etsy.com/listing/1097017861/personalized-name-necklace-gift-for-her?click_key=d7f18159fa6f923fa71cbe555281b2dae335bc31%3A1097017861&click_sum=f2c6ff6b&ref=hp_prn-3&pro=1&frs=1&sts=1', 
                   'https://poshmark.com/listing/Armani-collezioni-mens-black-gray-pinstripe-suit-jacket-made-in-Italy-size-42-6469a806db3a6f694f7ce07d', 
                   'https://www.amazon.com/Attract-Trilogy-RND-CZWH-RHS/dp/B07DPRW46T/ref=lp_63337800011_1_1?th=1', 
                   'https://www.asos.com/us/new-look/new-look-raglan-sleeve-crew-neck-sweatshirt-in-navy/prd/204190939?clr=navy&colourWayId=204190940&cid=27110', 
                   'https://www.macys.com/shop/product/jones-new-york-womens-short-sleeve-button-detail-top?ID=15955236&CategoryID=255&swatchColor=Bright%20Orchid%20Purple',
                   'https://www.uniqlo.com/us/en/products/E456191-000/00?colorDisplayCode=01&sizeDisplayCode=003', 
                   'https://www.gap.com/browse/product.do?pid=665485012&cid=8792&pcid=8792&vid=1#pdp-page-content', 
                   'https://www.nordstrom.com/s/on-running-cloudnova-flux-sneaker-women/7366346?origin=category-personalizedsort&breadcrumb=Home%2FWomen%2FNew%20Arrivals%2FShoes&color=101',
                   'https://www.jcpenney.com/p/worthington-womens-v-neck-elbow-sleeve-pullover-sweater/ppr5008328887?pTmplType=regular&deptId=dept20000013&catId=cat100210007&urlState=%2Fg%2Fwomen%2Fsweaters-cardigans%3Fid%3Dcat100210007&productGridView=medium&badge=new%7Cpetite&cm_re=ZI-_-DEPARTMENT-WOMEN-_-VN-_-CATEGORY-_-SWEATERS_4', 
                   'https://www.ajio.com/baggit-colourblock-sling-bag-with-adjustable-strap/p/4932381350_multi', 
                   'https://www.tobi.com/product/76266-tobi-carmen-belted-romper?color_id=108411', 
                   'https://www.nastygal.com/tassel-beaded-mini-shift-dress/BGG02297.html?color=174',
                   'https://www.everlane.com/products/womens-organic-pulll-on-short-sandstone?collection=womens-bestsellersv2', 
                   'https://modcloth.com/products/taking-the-day-hi-lo-midi-dress-nvy?variant=42668986073259', 
                   'https://www.revolve.com/beach-riot-camilla-bikini-top-in-black/dp/BRIO-WX677/?d=Womens&page=1&lc=8&itrownum=2&itcurrpage=1&itview=05', 
                   'https://www.zappos.com/p/wacoal-understated-cotton-hi-cut-orchid-petal-stripe/product/9849539/color/1047189',
                   'https://www.loft.com/clothing/tops/catl000011/613459.html?priceSort=DES',
                   'https://www.urbanoutfitters.com/shop/urban-renewal-made-in-la-eco-linen-maxi-skirt?category=skirts&color=030&type=REGULAR&quantity=1', 
                   'https://www.forever21.com/us/2000481077.html?dwvar_2000481077_color=02',
                   'https://www.francescas.com/product/26CA60QPXD/kaylee-off-the-shoulder-palm-print-romper',
                   'https://cacique.lanebryant.com/swim-brief/prd-399686.html?dwvar_399686_color=0000108059&catid=cat821001',
                   'https://oldnavy.gap.com/browse/product.do?pid=539541002&cid=26190&pcid=26190&vid=1&cpos=0&kcid=CategoryIDs%3D26190&ctype=Listing&cpid=res638199334316291808&ccam=21567#pdp-page-content', 
                   'https://www.fashionnova.com/products/oceanside-affair-1-piece-bikini-jade', 
                   'https://www.target.com/p/women-s-flutter-short-sleeve-dress-universal-thread/-/A-87567817?preselect=87460239#lnk=sametab', 
                   'https://www.freepeople.com/shop/lyla-linen-trousers/?category=trendspotting-western-femme&color=224&type=REGULAR&quantity=1',
                   'https://www.ae.com/us/en/p/women/tops/tank-tops/ae-one-shoulder-tank-top/0366_5597_500?menu=cat4840004', 
                   'https://www.aritzia.com/us/en/product/generation-blazer/104959.html?dwvar_104959_color=10006', 
                   'https://www.thereformation.com/products/chania-silk-dress/1310188VLL.html', 
                   'https://savedbythedress.com/collections/maternity/products/black-maternity-maxi-dress-with-slit-and-short-sleeves-11',
                   'https://www.bloomingdales.com/shop/product/aqua-fringed-knit-bodycon-midi-dress-100-exclusive?ID=4697714&CategoryID=1195659',
                   'https://www.anthropologie.com/shop/suboo-frida-plunge-maxi-dress?category=resort-wear&color=266&type=STANDARD&quantity=1', 
                   'https://tjmaxx.tjx.com/store/jump/product/women/Made-In-Italy-14k-Gold-Gothic-Initial-Signet-Ring/1000784298?colorId=NS11120694&pos=1:10&N=2107733895', 
                   'https://www.bershka.com/us/elastic-denim-jumpsuit-with-cut-out-back-c0p137699688.html?colorId=800&stylismId=2', 
                   'https://www.farmrio.com/products/beach-toucans-scarf-lenzing-ecovero-viscose-kimono',
                   'https://www.journelle.com/products/onl-10011-wild-rose-print?variant=42339167764659', 
                   'https://www.yandy.com/products/naughty-nights-tube-chemise-set', 
                   'https://www.savagex.com/shop/baroque-bondage-open-back-brazilian-ud2148800-0687-12089320?psrc=featured_categories_best-sellers', 
                   'https://www.bergdorfgoodman.com/p/chloe-arlene-small-grained-leather-saddle-crossbody-bag-prod180680058?icid=BGWS-HP-R2-XXXX-XXXXXXXXXXXXXXXX-NA-WhatsNew_051623',
                   'https://www.shopbop.com/scorpian-sunglasses-aire/vp/v=1/1504955196.htm?os=false&breadcrumb=Shop+Women%27s%3EOur+Favorites%3ESummer+%2723+Trend+Edit%3ECool+Shades&folderID=71668&colorSin=2055665417&fm=other-viewall&pf_rd_p=PLACEMENT_ID_PLACEHOLDER&pf_rd_r=IMPRESSION_REQUEST_ID_PLACEHOLDER&ref_=SB_PLP_PDP_W_BOUTI_SUMME_71668_NB_5',
                   'https://www.peek-cloppenburg.de/de/stylebop/p/baum-pferdgarten-crop-top-mit-allover-logo-hellgruen-1835414', 
                   'https://www.neimanmarcus.com/p/alice-olivia-abella-abstract-pleated-puff-sleeve-sweater-prod261700186?icid=NMWS_HP_XXXX_SPXX_ALOVXXXXXXXXXXXX_NAXXXXXX_HPNewArrivals_051223', 
                   'https://www.viviennewestwood.com/en/women/clothing/shirts-and-tops/metro-shirt-tinted-indigo-15010059W00HLK415.html', 
                   'https://www.alexandermcqueen.com/en-us/ready-to-wear/panelled-trench-coat-727441QFAAA2019.html',
                   'https://www.moschino.com/us_en/logo-lettering-python-print-loafers-blue-polma10362c1gmi5709.html'
                   'https://www.adidas.com/us/ultraboost-light-running-shoes/GY9352.html', 
                   'https://us.shein.com/EMERY-ROSE-Knot-Front-Pocket-Patched-Overall-Romper-Without-Tube-Top-p-10748193-cat-1860.html?src_identifier=fc%3DWomen%60sc%3DCLOTHING%60tc%3DJUMPSUITS%20%26%20BODYSUITS%60oc%3DJumpsuits%60ps%3Dtab01navbar05menu05dir01%60jc%3Dreal_1860&src_module=topcat&src_tab_page_id=page_home1685625317165&mallCode=1', 
                   'https://www.zara.com/us/en/convertible-crop-jacket-p04661815.html?v1=272715073&v2=2184220', 
                   'https://www.lulus.com/products/show-stopper-cream-embroidered-sequin-bodycon-midi-dress/856342.html',
                   'https://www.madewell.com/on/demandware.store/Sites-madewellUS-Site/en_US/Product-Multisell?externalProductCodes=NK023,NK842,NH399,NL556'
                   'https://www.macys.com/shop/product/levis-womens-726-high-rise-flare-jeans?ID=14231961&CategoryID=51475'
                   'https://www.express.com/clothing/women/stylist-super-high-waisted-pleated-pull-on-shorts/pro/03016256/color/RUM%20RAISIN/',
                   'https://www.uniqlo.com/us/en/products/E456191-000/00?colorDisplayCode=01&sizeDisplayCode=003'
                   ]


#Working Links to test for program regression
working_input_links = [  'https://www.nike.com/t/blazer-mid-pro-club-mens-shoes-Vgslvc/DQ7673-003',
                       'https://www2.hm.com/en_us/productpage.1195139001.html',
                       'https://www.urbanoutfitters.com/shop/urban-renewal-made-in-la-eco-linen-maxi-skirt?category=skirts&color=030&type=REGULAR&quantity=1',
                       'https://www.gap.com/browse/product.do?pid=665485012&cid=8792&pcid=8792&vid=1#pdp-page-content'
                    ]
