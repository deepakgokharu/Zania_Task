def register_blueprint(app):

    # registring the queries router here
    from app.routers import query_router
    app.register_blueprint(query_router.bp)