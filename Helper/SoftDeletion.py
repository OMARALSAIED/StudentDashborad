from MysqlModels.models import db
from datetime import datetime

class SoftDeleter:
    @staticmethod
    def soft_delete(model, object_id):
        """
        Soft deletes the record identified by object_id for the given model
        by setting the 'deleted' attribute to True and recording the deletion timestamp.
        """
        object_to_delete = model.query.get(object_id)

        if object_to_delete:
            object_to_delete.deleted = 1
            
            db.session.commit()  # Commit the changes to the database
            return True  # Return True to indicate successful soft deletion
        else:
            return False 