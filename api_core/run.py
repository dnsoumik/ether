from eve import Eve

settings = {'DOMAIN': {'people': {}}}

app = Eve(settings=settings)
app.run()
