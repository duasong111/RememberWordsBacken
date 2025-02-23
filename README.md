RememberWords Backend
This is the backend service for the "RememberWords" application, built with FastAPI. It provides APIs for word querying, recitation tracking, and story-related features. The project is designed to help users manage and memorize vocabulary efficiently.

项目结构
Part1: 单词管理和背诵的核心功能。
Part2: 故事和短语相关的功能。
API 端点
Part 1: 单词管理和背诵
查询和搜索
GET /Part1/search/query
搜索特定单词。
参数: 用于单词搜索的查询字符串。
GET /Part1/search/all
获取所有排名的单词。
GET /Part1/search/change
查询排名的单词（可能用于更新或排序）。
GET /Part1/search/gussWord
获取用于猜测的单词（可能是 "guess word"）。
背诵跟踪
GET /Part1/recite/getwords
获取用于背诵练习的单词。
GET /Part1/search/recite
增加单词的背诵次数。
GET /Part1/search/wrong
增加单词的错误次数。
分页和验证
GET /Part1/query
分页查询单词。
参数: 页码和限制数量。
GET /Part1/query/bool/conversion
查询时进行类型转换（例如布尔值）。
GET /Part1/query/validations
查询时进行参数验证。
GET /Part1/path_/{num}
路径参数验证。
路径参数: num (数字)。
城市和文件操作
GET /Part1/enum/{city}
获取特定城市相关数据。
路径参数: city (枚举值)。
GET /Part1/files/{file_path}
通过路径访问文件。
路径参数: file_path。
POST /Part1/request_body/city
提交城市信息。
请求体: 城市数据。
PUT /Part1/request_body/city/{name}
更新城市信息。
路径参数: name (城市名称)。
请求体: 更新后的城市数据。
PUT /Part1/request_body/nested
更新嵌套数据模型。
头部和 Cookie
GET /Part1/cookie
处理带有 Cookie 的数据获取。
GET /Part1/header
处理带有头部信息的验证和数据获取。
Part 2: 故事和短语功能
GET /Part2/search/phrase
获取故事中的短语或句子。
GET /Part2/story/picture
获取与故事相关的图片。
安装和运行
克隆仓库
bash
自动换行
复制
git clone https://github.com/duasong111/RememberWordsBacken.git
cd RememberWordsBacken
安装依赖 确保已安装 Python 3.7+，然后运行：
bash
自动换行
复制
pip install -r requirements.txt
运行应用
bash
自动换行
复制
uvicorn main:app --reload
API 将在 http://127.0.0.1:8000 上可用。
访问 API 文档 在浏览器中打开：
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
依赖
FastAPI
Uvicorn
（根据需要添加其他依赖）
贡献
欢迎提交问题或拉取请求来改进这个项目！