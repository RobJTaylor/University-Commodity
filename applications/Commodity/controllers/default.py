# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    product = db.products
    productName = product.product_name

    product1Name = ""
    product1URL = ""
    product1Image = ""
    product1Tag1 = ""
    product1Tag2 = ""
    product1Tag3 = ""

    product2Name = ""
    product2URL = ""
    product2Image = ""
    product2Tag1 = ""
    product2Tag2 = ""
    product2Tag3 = ""

    product3Name = ""
    product3URL = ""
    product3Image = ""
    product3Tag1 = ""
    product3Tag2 = ""
    product3Tag3 = ""

    i = 0
    for row in db().select(db.products.ALL, limitby=(0,3), orderby=~db.products.time_stamp):
        if i == 0:
            product1Name = row.product_name
            product1Image = row.product_image
            product1URL = URL('viewProduct', vars=dict(productID=row.id))
            product1Tag1 = row.tag_1
            product1Tag2 = row.tag_2
            product1Tag3 = row.tag_3
            i = i + 1
        elif i == 1:
            product2Name = row.product_name
            product2Image = row.product_image
            product2URL = URL('viewProduct', vars=dict(productID=row.id))
            product2Tag1 = row.tag_1
            product2Tag2 = row.tag_2
            product2Tag3 = row.tag_3
            i = i + 1
        elif i == 2:
            product3Name = row.product_name
            product3Image = row.product_image
            product3URL = URL('viewProduct', vars=dict(productID=row.id))
            product3Tag1 = row.tag_1
            product3Tag2 = row.tag_2
            product3Tag3 = row.tag_3
            i = i + 1
    return locals()

def newProduct():
    form = SQLFORM(db.products).process()
    return locals()

def addRetailer():
    form = SQLFORM(db.retailers).process()
    return locals()

def viewAllProducts():
    rows = db(db.products).select()
    return locals()

def viewProduct():
    product = db.products
    productID = product.id
    queryID = request.vars.productID
    query = productID == queryID
    search = db(query)
    rows = search.select()

    name = ""
    image = ""
    description = ""
    price = ""
    tag1 = ""
    tag2 = ""
    tag3 = ""
    timestamp = ""

    for row in rows:
        name = row.product_name
        image = row.product_image
        description = row.product_description
        price = row.product_price
        tag1 = row.tag_1
        tag2 = row.tag_2
        tag3 = row.tag_3
        timestamp = row.time_stamp

    reviews = db.reviews
    rProductID = reviews.products_id
    query = rProductID == request.vars.productID
    search = db(query)

    newRows = search.select()

    loggedIn = 0

    if not auth.is_logged_in():
        loggedIn = 0
    else:
        loggedIn = 1
        db.reviews.reviewer_name.default = auth.user.first_name

    db.reviews.products_id.default = request.vars.productID
    db.reviews.review_rating.default = 0
    form = SQLFORM(db.reviews).process()

    return locals()

def upvote():
    reviews = db.reviews
    reviewID = reviews.id
    query = reviewID == request.args[0]
    search = db(query)
    rows = search.select()

    for row in rows:
        reviewRating = row.review_rating
        reviewRating = reviewRating + 1
        row.update_record(review_rating=reviewRating)

    return locals()

def downvote():
    reviews = db.reviews
    reviewID = reviews.id
    query = reviewID == request.args[0]
    search = db(query)
    rows = search.select()

    for row in rows:
        reviewRating = row.review_rating
        reviewRating = reviewRating - 1
        row.update_record(review_rating=reviewRating)

    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
