# Association table for many-to-many relationship between User and Role
user_roles = db.Table(
    'user_roles',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('role_id',
              db.Integer,
              db.ForeignKey('roles.id', ondelete='CASCADE'),
              primary_key=True))
