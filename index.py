from shorten import shorten
import wget
import pprint
from pymongo import MongoClient
from docxtpl import DocxTemplate,R, InlineImage
from docx.shared import Mm,Inches
import os
from PIL import Image
from decouple import config
from pdf import convert_to
client = MongoClient(config('MONGO_HOST'))
context = {"name":config('NAME'),"from":config('FROM'),"contact":config('CONTACT'),"projects":[]}
db = client['resume']
projects=db.resumes
images=[]
doc = DocxTemplate("resume.docx")
for post in projects.find().sort("_id",-1):
   imajin=InlineImage(doc, "a.jpg", height=Inches(3.97),width=Inches(6.25))
   if post['i']:
       image_filename = wget.download(post['i'])
       foo = Image.open(image_filename)
       im=foo.convert('RGB')
       im.save(image_filename+".jpg","JPEG",optimize=True,quality=65)
       images.append(image_filename)
       images.append(image_filename+".jpg")       
       imajin=InlineImage(doc, image_filename+".jpg", height=Inches(3.97),width=Inches(6.25))
   context['projects'].append({"page_break":R('\f'),'description':post['d'],'title':post['t'],'year':'2019','role':'programmer','link':shorten(post['p'],post['t']) if post['p'] else shorten(post['g'],post['t']) if post['g'] and post['t'] else '-' 
   ,'image':imajin})

doc.render(context)
doc.save("generated_resume.docx")
for image in images:
    os.remove(image)
convert_to("./","generated_resume.docx")
os.remove("generated_resume.docx")
