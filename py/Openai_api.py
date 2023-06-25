import os
import openai

API_KEY = 'Your API_KEY'
os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")
def query(text):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="### Postgres SQL with PostGIS extension tables use ST_INTERSECTS,ST_TOUCHES,ST_AREA,ST_LENGTH,ST_DISTANCE\n#All queries start with SELECT id,geom,name \n# with their properties:\n# poi(id,geom,name)contains Nanjing Jiangning Tangshan National Geopark\n# river(id,geom,name)\n# district(id,geom,name)contains Gulou district\n# lakes(id,geom,name) contains lakes\n# street(id,geom,name)\n# subway(id,geom,name)\n# water(id,geom,name) contains Reservoirs\n#\n###A query to "+text+"\n",
    temperature=0,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["#", ";"])
    answer = response["choices"][0]["text"]
    return answer