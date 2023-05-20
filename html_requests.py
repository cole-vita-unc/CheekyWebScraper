import requests
from bs4 import BeautifulSoup

# List of links working 
all_input_links = ['https://www.nike.com/t/blazer-mid-pro-club-mens-shoes-Vgslvc/DQ7673-003', 
                   'https://www2.hm.com/en_us/productpage.1195139001.html', 
                   'https://fearofgod.com/collections/essentials/products/sp23-ss-sweatshirt-off-black', 
                   'https://www.etsy.com/listing/1097017861/personalized-name-necklace-gift-for-her?click_key=d7f18159fa6f923fa71cbe555281b2dae335bc31%3A1097017861&click_sum=f2c6ff6b&ref=hp_prn-3&pro=1&frs=1&sts=1', 
                   'https://poshmark.com/listing/NIKE-Air-Force-1-Low-LV8-1Womens-75-CW0984100-644e8a86943ddbaf5263ddf4', 
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
                   'https://www.express.com/clothing/women/satin-crew-neck-gramercy-tee/pro/08628854/color/Pecan/',
                   'https://www.farmrio.com/products/beach-toucans-scarf-lenzing-ecovero-viscose-kimono',
                   'https://www.journelle.com/products/onl-10011-wild-rose-print?variant=42339167764659', 
                   'https://www.yandy.com/products/naughty-nights-tube-chemise-set', 
                   'https://www.savagex.com/shop/baroque-bondage-open-back-brazilian-ud2148800-0687-12089320?psrc=featured_categories_best-sellers', 
                   'https://www.bergdorfgoodman.com/p/chloe-arlene-small-grained-leather-saddle-crossbody-bag-prod180680058?icid=BGWS-HP-R2-XXXX-XXXXXXXXXXXXXXXX-NA-WhatsNew_051623',
                   'https://www.shopbop.com/scorpian-sunglasses-aire/vp/v=1/1504955196.htm?os=false&breadcrumb=Shop+Women%27s%3EOur+Favorites%3ESummer+%2723+Trend+Edit%3ECool+Shades&folderID=71668&colorSin=2055665417&fm=other-viewall&pf_rd_p=PLACEMENT_ID_PLACEHOLDER&pf_rd_r=IMPRESSION_REQUEST_ID_PLACEHOLDER&ref_=SB_PLP_PDP_W_BOUTI_SUMME_71668_NB_5'
                   ]


input_links = ['https://www.peek-cloppenburg.de/de/stylebop/p/baum-pferdgarten-crop-top-mit-allover-logo-hellgruen-1835414', 
               'https://www.neimanmarcus.com/p/alice-olivia-abella-abstract-pleated-puff-sleeve-sweater-prod261700186?icid=NMWS_HP_XXXX_SPXX_ALOVXXXXXXXXXXXX_NAXXXXXX_HPNewArrivals_051223', 
               'https://www.viviennewestwood.com/en/women/clothing/shirts-and-tops/metro-shirt-tinted-indigo-15010059W00HLK415.html', 
               'https://www.alexandermcqueen.com/en-us/ready-to-wear/panelled-trench-coat-727441QFAAA2019.html',
               'https://www.moschino.com/us_en/logo-lettering-python-print-loafers-blue-polma10362c1gmi5709.html']

# Empty list to store the resulting HTML
output_html = []

#Create active session to access links with a header 
s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
})


for link in input_links:
    try:
        # Use requests to get the page content
        response = s.get(link)
        
        # Check if request was successful
        response.raise_for_status()
    except requests.HTTPError as http_err:
        output_html.append(None)
        print(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        output_html.append(None)
        print(f'Other error occurred: {err}')
    else:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Add the parsed HTML to your output list
        output_html.append(soup.prettify())

# Now input_links[i] corresponds to output_html[i]
for i in range(len(input_links)):
    if output_html[i] is None:
         print(f'HTML content of {input_links[i]} was not retrieved')
    #else:
        #print(f'HTML content of {input_links[i]} is stored in output_html[{i}]')

#with open(f'output_1.txt', 'w') as f:
#            f.write(soup.prettify())