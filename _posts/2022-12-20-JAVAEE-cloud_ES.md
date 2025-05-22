---
categories: [javaEE]
tags: [ElasticSearch]
---
# ElasticSearch

- ELK技术栈
  - kibana
  - Logstash
  - Beats
  
- elasticsearch底层是基于**lucene**来实现的。**Lucene**是一个Java语言的搜索引擎类库

- 正向和倒排
  - **正向索引**是最传统的，根据id索引的方式。但根据词条查询时，必须先逐条获取每个文档，然后判断文档中是否包含所需要的词条，是**根据文档找词条的过程**。
    - 优点：
      - 可以给多个字段创建索引
      - 根据索引字段搜索、排序速度非常快
    - 缺点：
      - 根据非索引字段，或者索引字段中的部分词条查找时，只能全表扫描。
  - 而**倒排索引**则相反，是先找到用户要搜索的词条，根据词条得到保护词条的文档的id，然后根据id获取文档。是**根据词条找文档的过程**。
    - 优点：
      - 根据词条搜索、模糊搜索时，速度非常快
    - 缺点：
      - 只能给词条创建索引，而不是字段
      - 无法根据字段做排序

- 倒排索引

  - 创建
    - 将每一个文档的数据利用算法分词，得到一个个词条
    - 创建表，每行数据包括词条、词条所在文档id、位置等信息
    - 因为词条唯一性，可以给词条创建索引，例如hash表结构索引
  - 搜索
    - 用户输入条件`"华为手机"`进行搜索。
    - 对用户输入内容**分词**，得到词条：`华为`、`手机`。
    - 拿着词条在倒排索引中查找，可以得到包含词条的文档id：1、2、3。
    - 拿着文档id到正向索引中查找具体文档。

- elasticsearch索引库

  - 约束

    - **映射（mapping）**
      - type：字段数据类型，常见的简单类型有：
        - 字符串：text（可分词的文本）、keyword（精确值，例如：品牌、国家、ip地址）
        - 数值：long、integer、short、byte、double、float、
        - 布尔：boolean
        - 日期：date
        - 对象：object
      - index：是否创建索引，默认为true
      - analyzer：使用哪种分词器
      - properties：该字段的子字段

  - CRUD

    - ```
      DSL
      创建索引库和映射
      PUT /索引库名称
      {
        "mappings": {
          "properties": {
            "字段名":{
              "type": "text",
              "analyzer": "ik_smart"
            },
            "字段名2":{
              "type": "keyword",
              "index": "false"
            },
            "字段名3":{
              "properties": {
                "子字段": {
                  "type": "keyword"
                }
              }
            }
          }
        }
      }
      查询索引库
      GET /NAME
      修改索引库
      倒排索引结构虽然不复杂，但是一旦数据结构改变（比如改变了分词器），就需要重新创建倒排索引，这简直是灾难。因此索引库**一旦创建，无法修改mapping**。
      新增
      PUT /索引库名/_mapping
      {
        "properties": {
          "新字段名":{
            "type": "integer"
          }
        }
      }
      删除索引库
      DELETE /索引库名
      新增文档
      POST /索引库名/_doc/文档id
      {
          "字段1": "值1",
          "字段2": "值2",
          "字段3": {
              "子属性1": "值3",
              "子属性2": "值4"
          },
          // ...
      }
      查询文档
      GET /{索引库名称}/_doc/{id}
      删除文档
      DELETE /{索引库名}/_doc/id值
      修改文档
      	全量修改
      		- 根据指定的id删除文档
      		- 新增一个相同id的文档
      	PUT /{索引库名}/_doc/文档id
          {
              "字段1": "值1",
              "字段2": "值2",
              // ... 略
          }
          增量修改
          POST /{索引库名}/_update/文档id
          {
              "doc": {
                   "字段名": "新的值",
              }
          }
      ```

  - RestClient操作文档

    - 初始化RestHighLevelClient

    - 创建XxxRequest。XXX是Index、Get、Update、Delete、Bulk

    - 准备参数（Index、Update、Bulk时需要）

    - 发送请求。调用RestHighLevelClient#.xxx()方法，xxx是index、get、update、delete、bulk

    - 解析结果（Get时需要）

    - ```
      @Test
      void testAddDocument() throws IOException {
          // 1.准备Request对象
          IndexRequest request = new IndexRequest("hotel").id(hotelDoc.getId().toString());
          // 2.准备Json文档
          request.source(json, XContentType.JSON);
          // 3.发送请求
          SearchResponse response = client.search(request, RequestOptions.DEFAULT);
          // 4.解析响应
          String json = response.getSourceAsString();
          client.delete(request, RequestOptions.DEFAULT);
          handleResponse(response);
      }
      ```

  - DSL查询

    - ```
      GET /indexName/_search
      {
        "query": {
          "查询类型(match_all/match/term/...)": {
            "查询条件": "条件值"
          }
        }
      }
      ```

    - **查询所有**：查询出所有数据，一般测试用。例如：match_all

    - **全文检索（full text）查询**：利用分词器对用户输入内容分词，然后去倒排索引库中匹配。例如：

      - match_query,multi_match_query

    - **精确查询**：根据精确词条值查找数据，一般是查找keyword、数值、日期、boolean等类型字段。例如：因为精确查询的字段搜是不分词的字段，因此查询的条件也必须是**不分词**的词条。查询时，用户输入的内容跟自动值完全匹配时才认为符合条件。如果用户输入的内容过多，反而搜索不到数据。

      - ids,range,term

    - **地理（geo）查询**：根据经纬度查询。例如：

      - geo_distance距离查询圆形范围内,geo_bounding_box矩形范围查询

    - **复合（compound）查询**：复合查询可以将上述各种查询条件组合起来，合并查询条件。例如：

      - bool
      - function_score
        - 1）根据**原始条件**查询搜索文档，并且计算相关性算分，称为**原始算分**（query score）
        - 2）根据**过滤条件**，过滤文档
        - 3）符合**过滤条件**的文档，基于**算分函数**运算，得到**函数算分**（function score）
        - 4）将**原始算分**（query score）和**函数算分**（function score）基于**运算模式**做运算，得到最终结果，作为相关性算分。
        - ![1679377603108](../../../../img/1679377603108.png)

  - DSL查询结果

    - ```
      @Test
      void testAddDocument() throws IOException {
      
          // 1.准备Request
          SearchRequest request = new SearchRequest("hotel");
          // 2.准备DSL
          	request.source().query(QueryBuilders.matchQuery("all", "如家"));
              
              // 2.1.准备BooleanQuery
              BoolQueryBuilder boolQuery = QueryBuilders.boolQuery();
              // 2.2.添加term
              boolQuery.must(QueryBuilders.termQuery("city", "杭州"));
              // 2.3.添加range
              boolQuery.filter(QueryBuilders.rangeQuery("price").lte(250));
              request.source().query(boolQuery);
              
              // 2.1.query
              request.source().query(QueryBuilders.matchAllQuery());
              // 2.2.排序 sort
              request.source().sort("price", SortOrder.ASC);
              // 2.3.分页 from、size
              request.source().from((page - 1) * size).size(5);
          	
          	request.source().highlighter(new HighlightBuilder().field("name").requireFieldMatch(false));
          // 3.发送请求
          SearchResponse response = client.search(request, RequestOptions.DEFAULT);
          // 4.解析响应
          handleResponse(response);
      }
      ```

    - ```
      GET /indexName/_search
      {
        "query": {
          "match_all": {}
        },
        "from": 0, // 分页开始的位置，默认为0
        "size": 10, // 期望获取的文档总数
        "sort": [
          {
            "FIELD": "desc"  // 排序字段、排序方式ASC、DESC
          }
          "_geo_distance" : {
                "FIELD" : "纬度，经度", // 文档中geo_point类型的字段名、目标坐标点
                "order" : "asc", // 排序方式
                "unit" : "km" // 排序的距离单位
            }
        ]
        "highlight": {
          "fields": { // 指定要高亮的字段
            "FIELD": {
              "pre_tags": "<em>",  // 用来标记高亮字段的前置标签
              "post_tags": "</em>" // 用来标记高亮字段的后置标签
            }
          }
        }
      }
      ```

    - 深度分页：集群

      - search after：分页时需要排序，原理是从上一次的排序值开始，查询下一页数据。官方推荐使用的方式。
      - scroll：原理将排序后的文档id形成快照，保存在内存。官方已经不推荐使用。

- 数据聚合

  - ```
    // 酒店数据索引库
    PUT /hotel
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "text_anlyzer": {
              "tokenizer": "ik_max_word",
              "filter": "py"
            },
            "completion_analyzer": {
              "tokenizer": "keyword",
              "filter": "py"
            }
          },
          "filter": {
            "py": {
              "type": "pinyin",
              "keep_full_pinyin": false,
              "keep_joined_full_pinyin": true,
              "keep_original": true,
              "limit_first_letter_length": 16,
              "remove_duplicated_term": true,
              "none_chinese_pinyin_tokenize": false
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "id":{
            "type": "keyword"
          },
          "name":{
            "type": "text",
            "analyzer": "text_anlyzer",
            "search_analyzer": "ik_smart",
            "copy_to": "all"
          },
          "address":{
            "type": "keyword",
            "index": false
          },
          "price":{
            "type": "integer"
          },
          "score":{
            "type": "integer"
          },
          "brand":{
            "type": "keyword",
            "copy_to": "all"
          },
          "city":{
            "type": "keyword"
          },
          "starName":{
            "type": "keyword"
          },
          "business":{
            "type": "keyword",
            "copy_to": "all"
          },
          "location":{
            "type": "geo_point"
          },
          "pic":{
            "type": "keyword",
            "index": false
          },
          "all":{
            "type": "text",
            "analyzer": "text_anlyzer",
            "search_analyzer": "ik_smart"
          },
          "suggestion":{
              "type": "completion",
              "analyzer": "completion_analyzer"
          }
        }
      }
    }
    ```

- 数据同步

  - 同步调用
    - 优点：实现简单，粗暴
    - 缺点：业务耦合度高
  - 异步通知
    - 优点：低耦合，实现难度一般
    - 缺点：依赖mq的可靠性
  - 监听binlog
    - 优点：完全解除服务间耦合
- 缺点：开启binlog增加数据库负担、实现复杂度高
  
- 集群

  - 海量数据存储问题：将索引库从逻辑上拆分为N个分片（shard），存储到多个节点
  - 单点故障问题：将分片数据在不同节点备份（replica ）
  - 集群脑裂
    - 