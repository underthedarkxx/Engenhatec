from .. import db

class Material(db.Model):
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200))
    caption = db.Column(db.String(200))
    description = db.Column(db.Text)  # Corrigido: removeu parêntese extra
    category = db.Column(db.String(50))
    
    # Relacionamentos
    pros = db.relationship('Pro', backref='material', lazy=True, cascade="all, delete-orphan")
    cons = db.relationship('Con', backref='material', lazy=True, cascade="all, delete-orphan")
    brands = db.relationship('Brand', backref='material', lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_url': self.image_url,
            'caption': self.caption,
            'description': self.description,
            'category': self.category,
            'pros': [pro.to_dict() for pro in self.pros],
            'cons': [con.to_dict() for con in self.cons],
            'brands': [brand.to_dict() for brand in sorted(self.brands, key=lambda x: x.position)]
        }

class Pro(db.Model):
    __tablename__ = 'pros'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    pro_text = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'pro_text': self.pro_text
        }

class Con(db.Model):
    __tablename__ = 'cons'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    con_text = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'con_text': self.con_text
        }

class Brand(db.Model):
    __tablename__ = 'brands'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)
    price_observation = db.Column(db.String(100))
    website = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'position': self.position,
            'name': self.name,
            'rating': self.rating,
            'price_observation': self.price_observation,
            'website': self.website
        }
