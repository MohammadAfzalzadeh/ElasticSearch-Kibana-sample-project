# پروژه ElasticSearch & kibana 
- اعضای گروه :
    - محمد افضل زاده نائینی - 10
    - علی محمد طباطبائی - 10
    - محمدرضا مومنی یزدی - 10

## بخش صفر : اتصال به Elastic Search

فایل `elastic_connection.py` در این پروژه برای برقراری اتصال به سرویس Elasticsearch استفاده می‌شود. این فایل شامل تنظیمات اتصال به Elasticsearch و یک تابع برای اجرای پرس و جوهای Elasticsearch است. در اینجا توضیحات کوتاهی درباره هر قسمت این فایل آمده است:


1. **اتصال به Elasticsearch:**
   در این بخش، یک اتصال به Elasticsearch ایجاد شده است با مشخصات زیر:
   - آدرس `https://localhost:9200` برای اتصال به سرویس Elasticsearch محلی.
   - `verify_certs=False` برای غیرفعال کردن تأیید صحت گواهی‌نامه SSL.
   - `ca_certs="/path/to/ca.crt"` برای مشخص کردن مسیر فایل گواهی‌نامه CA (در صورت نیاز).
   - `api_key` برای استفاده از کلید API برای احراز هویت.

2. **تابع `run_elastic_query`:**
   این تابع برای اجرای یک پرس و جو در Elasticsearch استفاده می‌شود و نتایج را به صورت لیستی از مستندات (documents) برمی‌گرداند که از نتایج جستجو به دست آمده‌اند.

این فایل به عنوان یک ماژول جداگانه در کل پروژه استفاده می‌شود تا اتصال به Elasticsearch را مدیریت کرده و پرس و جوهای مورد نیاز را اجرا کند.

این بخش اول پروژه به تحلیل داده‌های JSON می‌پردازد و آن‌ها را به Elasticsearch ارسال می‌کند. در این بخش، کدهای زیر اجرا می‌شوند:

## بخش اول - تحلیل داده‌های JSON و ارسال به Elasticsearch

1. **توضیحات Docker:**

راه اندازی الاستیک سرچ و کیبانا با داکر
   ```bash
   docker run --name es01   --rm  -it --net elastic -p 9200:9200 -m 1GB  docker.arvancloud.ir/elasticsearch:8.13.4

    docker run --name kib01  --rm      --net elastic -p 5601:5601   docker.arvancloud.ir/kibana:8.13.4
   ```


2. **توابع مربوط به پردازش داده‌ها:**
   - `convert_votes_to_int(votes_str)`: تابعی است که رشته‌ای حاوی امتیازها را به عدد صحیح تبدیل می‌کند.
   - `process_json_file(file_path)`: این تابع یک فایل JSON را باز می‌کند، داده‌ها را تحلیل می‌کند و اگر می‌تواند امتیازها را تبدیل کند، انجام می‌دهد.
   - `read_and_convert_votes(directory)`: این تابع به طول می‌انجامد تا تمام فایل‌های JSON در یک دایرکتوری مشخص را بخواند و آن‌ها را برای تحلیل و ارسال به Elasticsearch آماده کند.

3. **ارسال داده‌ها به Elasticsearch:**
   ```python
   directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
   articles = read_and_convert_votes(directory_path)

   for article in articles:
       es.index(index="articles", document=article)
   ```
   - در این بخش، تمام مقالاتی که از فایل‌های JSON خوانده شده‌اند، به Elasticsearch ارسال می‌شوند. این ارسال با استفاده از شی `es` که از فایل `elastic_connection.py` import شده است، انجام می‌شود.



### بخش دوم - اجرای پرس و جو در Elasticsearch و ذخیره نتایج

1. **Import و تنظیم مسیرها:**

2. **تعریف پرس و جو:**
   ```python
   # Define the query
   query = {
       "query": {
           "match": {
               "Title": "ethereum"
           }
       }
   }
   ```
   - در اینجا یک پرس و جو ساده برای جستجوی عبارت "ethereum" در فیلد "Title" تعریف شده است.

3. **اجرای پرس و جو و ذخیره نتایج:**

   - این بخش شامل اجرای پرس و جو با استفاده از تابع `run_elastic_query` که در فایل `elastic_connection.py` تعریف شده است.
   - نتایج پرس و جو به فرمت JSON با استفاده از کتابخانه `json` ذخیره می‌شوند و در فایل `query_result.json` ذخیره می‌شوند.
   - پیامی نمایش داده می‌شود که نتایج پرس و جو در فایل `query_result.json` ذخیره شده است.

این بخش از پروژه برای اجرای پرس و جو در Elasticsearch با استفاده از یک فایل `elastic_connection.py` جهت جستجوی "ethereum" در فیلد "Title" طراحی شده است و نتایج را در یک فایل JSON ذخیره می‌کند.

[query-result](./Phase2/query_result.json)

همچنین در این کوئری با ابزار kibana هم انجام شده است 
![kibana Query](./Phase2/Kibana%20Search.png)

## بخش سوم : کوئری پیچیده
کد JavaScript در این بخش برای امکان تعریف و ارسال جستجوهای پیچیده به Elasticsearch استفاده می‌شود. این کد امکانات زیر را برای کاربر فراهم می‌کند:

1. **افزودن و حذف گروه‌های جستجو:** کاربر می‌تواند با دکمه‌های "Add" و "Remove"، گروه‌های جستجو را به فرم اضافه یا حذف کند. این امکان به کاربر اجازه می‌دهد تا جستجوهای متعدد و پیچیده‌تری را برای Elasticsearch تعریف کند.

2. **انتخاب عملگر منطقی (Boolean Operator):** هر گروه جستجو دارای یک عملگر منطقی مانند "AND"، "OR" یا "NOT" است که کاربر می‌تواند بر اساس آنها ارتباطات مختلفی بین شروط جستجو را تعیین کند.

3. **انتخاب فیلد (Metadata):** کاربر می‌تواند فیلد مورد نظر برای جستجو را از بین گزینه‌هایی مانند "abstract"، "IEEE keywords"، "DOI" و "Title" انتخاب کند. این انتخاب به کاربر امکان می‌دهد تا منطقی‌ترین فیلد برای جستجوی اطلاعات مورد نظر را انتخاب کند.

4. **ساختار JSON برای Elasticsearch:** پس از جمع‌آوری اطلاعات مورد نیاز، یک ساختار JSON برای ارسال به Elasticsearch ایجاد می‌شود. این ساختار شامل شرایط "must"، "should" و "must_not" برای استفاده در یک کوئری Elasticsearch است که بر اساس انتخاب‌های کاربر تشکیل می‌شود.

5. **ارسال کوئری به سرور Flask:** پس از تشکیل کامل کوئری Elasticsearch، کوئری به سرور Flask ارسال می‌شود. سرور Flask با استفاده از کتابخانه‌های مربوطه، کوئری را به Elasticsearch ارسال کرده و نتایج را برمی‌گرداند.

این روند به کاربر این امکان را می‌دهد تا با دقت بیشتر و بر اساس نیاز خود، جستجوهای پیچیده‌تری را برای Elasticsearch تعریف کرده و نتایج مورد انتظار خود را از سیستم بازیابی اطلاعات دریافت کند.

پس از دریافت کوئری کاربر آن را مجدد به یک index دیگر اضافه می کنیم تا داشبورد های kibana را برای آن داشته باشیم 
- داشبورد برای همه داده ها
![main-dashboard](./Phase3/Dashboard%20images/Article%20Dashboard.png)
- داشبورد برای داده های مورد نیاز کاربر
![selected-dashboard](./Phase3/Dashboard%20images/new%20Article%20Dashboard.png)

[exportedDashboard](./Phase3/exportedDashboard.ndjson)

نتایج اجرا : 
![](./Phase3/Run%20Images/frontPage.png)
![](./Phase3/Run%20Images/new%20Index%20with%20search.png)
![](./Phase3/Run%20Images/new%20index.png)

## بخش چهارم : سیستم بازیابی اطلاعات بر اساس TF-IDF و Cosine Similarity
فایل‌ها و بخش‌ها
1. elastic_connection.py
این فایل شامل کد ارتباط با Elasticsearch و اجرای کوئری‌های مختلف است.

run_elastic_query(query): تابع برای اجرای کوئری‌های Elasticsearch و بازگرداندن نتایج.
2. main.py
این فایل شامل کدهای اصلی برای محاسبه TF-IDF، Cosine Similarity و اجرای سرور Flask برای نمایش نتایج به کاربر می‌باشد.

get_all_data(): بازگرداندن تمام داده‌های موجود در Elasticsearch.
get_specific_data(doi): بازگرداندن داده‌های خاص بر اساس شناسه DOI.
calculate_tfidf(texts): محاسبه TF-IDF برای متن‌ها.
calculate_similarity_and_scores(): محاسبه شباهت و امتیازهای نهایی بر اساس TF-IDF و Cosine Similarity.
3. Templates: index.html و results.html
این دو فایل HTML شامل قالب‌های صفحات وب برای ورود به سایت و نمایش نتایج می‌باشد

-  : نتایج اجرا

![](./Phase4/run%20Images/rs%20query.png)
![](./Phase4/run%20Images/result.png)