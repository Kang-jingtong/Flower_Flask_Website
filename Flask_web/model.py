from app import db
import json


class Users(db.Model):
    __tablename__ = 'Users'
    phoneNumber = db.Column(db.String(64),primary_key=True)
    nickName = db.Column(db.String(64),index=True)
    realName = db.Column(db.String(64),index=True)
    Sex = db.Column(db.Integer)
    Profile = db.Column(db.String(512))
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<Users{}>'.format(self.phoneNumber)


class Locations(db.Model):
    __tablename__ = 'Locations'
    phoneNumber = db.Column(db.String(64),db.ForeignKey('Users.phoneNumber'),primary_key=True)
    Location = db.Column(db.String(128),primary_key=True)

    def __repr__(self):
        return '<Locations{}>'.format(self.phoneNumber)


class COrders(db.Model):
    __tablename__ = 'COrders'
    phoneNumber = db.Column(db.String(64),db.ForeignKey('Users.phoneNumber'))
    orderNumber = db.Column(db.String(64), primary_key=True)
    realName = db.Column(db.String(64))
    orderMode = db.Column(db.String(32))
    orderType = db.Column(db.String(32))
    orderDate = db.Column(db.String(32))
    orderRemark = db.Column(db.String(128))
    orderLocation = db.Column(db.String(128))

    def __repr__(self):
        return '<COrders{}>'.format(self.orderNumber)


class CFlowers(db.Model):
    __tablename__ = 'CFlowers'
    flowerNumber = db.Column(db.String(64),primary_key=True)
    flowerName = db.Column(db.String(128))
    Useage = db.Column(db.String(128))
    Storage = db.Column(db.Integer)
    Price = db.Column(db.Float)
    Picture = db.Column(db.String(256))
    Color = db.Column(db.String(32))
    Material = db.Column(db.String(64))
    maxPrice = db.Column(db.Float)
    minPrice = db.Column(db.Float)
    Discription = db.Column(db.String(256))

    def __repr__(self):
        return '<CFlowers{}>'.format(self.flowerNumber)


class CflowerOrders(db.Model):
    __tablename__ = 'CflowerOrders'
    flowerNumber = db.Column(db.String(64),db.ForeignKey('CFlowers.flowerNumber'),primary_key=True)
    orderNumber = db.Column(db.String(64),db.ForeignKey('COrders.orderNumber'),primary_key=True)
    flowerQuantity = db.Column(db.Integer)

    def __repr__(self):
        return '<CflowerOrders{}>'.format(self.orderNumber)


class CcartOfSingleType(db.Model):
    __tablename__ = 'CcartOfSingleType'
    cartNumber = db.Column(db.String(64),primary_key=True)
    phoneNumber = db.Column(db.String(64))
    flowerNumber = db.Column(db.String(64))
    buyNumber = db.Column(db.Integer)

    def __repr__(self):
        return '<CcartOfSingleType{}>'.format(self.cartNumber)


class CcartOfMultiType(db.Model):
    __tablename__ = 'CcartOfMultiType'
    cartNumber = db.Column(db.String(64), primary_key=True)
    phoneNumber = db.Column(db.String(64))
    combineNumber = db.Column(db.String(64))
    buyNumber = db.Column(db.Integer)

    def __repr__(self):
        return '<CcartOfMultiType{}>'.format(self.cartNumber)


class CflowerCombines(db.Model):
    __tablename__ = 'CflowerCombines'
    combineNumber = db.Column(db.String(64),primary_key=True)
    Name = db.Column(db.String(128))
    Image = db.Column(db.String(256))
    Price = db.Column(db.Float)
    Tags = db.Column(db.String(128))
    Discription = db.Column(db.String(256))

    def __repr__(self):
        return '<CflowerCombines{}>'.format(self.combineNumber)


class CflowerCombineOrders(db.Model):
    __tablename__ = 'CflowerCombineOrders'
    combineNumber = db.Column(db.String(64),db.ForeignKey('CflowerCombines.combineNumber'),primary_key=True)
    orderNumber = db.Column(db.String(64),db.ForeignKey('COrders.orderNumber'),primary_key=True)
    buyQuantity = db.Column(db.Integer)

    def __repr__(self):
        return '<CflowerCombineOrders{}>'.format(self.orderNumber)




#--------------English Version----------------



class EOrders(db.Model):
    __tablename__ = 'EOrders'
    phoneNumber = db.Column(db.String(64),db.ForeignKey('Users.phoneNumber'))
    orderNumber = db.Column(db.String(64), primary_key=True)
    realName = db.Column(db.String(64))
    orderMode = db.Column(db.String(32))
    orderType = db.Column(db.String(32))
    orderDate = db.Column(db.String(32))
    orderRemark = db.Column(db.String(128))
    orderLocation = db.Column(db.String(128))
    def __repr__(self):
        return '<EOrders{}>'.format(self.orderNumber)


class EFlowers(db.Model):
    __tablename__ = 'EFlowers'
    flowerNumber = db.Column(db.String(64),primary_key=True)
    flowerName = db.Column(db.String(128))
    Useage = db.Column(db.String(128))
    Storage = db.Column(db.Integer)
    Price = db.Column(db.Float)
    Picture = db.Column(db.String(512))
    Color = db.Column(db.String(32))
    Material = db.Column(db.String(64))
    maxPrice = db.Column(db.Float)
    minPrice = db.Column(db.Float)
    Discription = db.Column(db.String(256))
    def __repr__(self):
        return '<EFlowers{}>'.format(self.flowerNumber)


class EflowerOrders(db.Model):
    __tablename__ = 'EflowerOrders'
    flowerNumber = db.Column(db.String(64),db.ForeignKey('EFlowers.flowerNumber'),primary_key=True)
    orderNumber = db.Column(db.String(64),db.ForeignKey('EOrders.orderNumber'),primary_key=True)
    flowerQuantity = db.Column(db.Integer)
    def __repr__(self):
        return '<EflowerOrders{}>'.format(self.orderNumber)

class EcartOfSingleType(db.Model):
    __tablename__ = 'EcartOfSingleType'
    cartNumber = db.Column(db.String(64), primary_key=True)
    phoneNumber = db.Column(db.String(64))
    flowerNumber = db.Column(db.String(64))
    buyNumber = db.Column(db.Integer)
    def __repr__(self):
        return '<EcartOfSingleType{}>'.format(self.cartNumber)
class EcartOfMultiType(db.Model):
    __tablename__ = 'EcartOfMultiType'
    cartNumber = db.Column(db.String(64), primary_key=True)
    phoneNumber = db.Column(db.String(64))
    combineNumber = db.Column(db.String(64))
    buyNumber = db.Column(db.Integer)
    def __repr__(self):
        return '<EcartOfMultiType{}>'.format(self.cartNumber)

class EflowerCombines(db.Model):
    __tablename__ = 'EflowerCombines'
    combineNumber = db.Column(db.String(64),primary_key=True)
    Name = db.Column(db.String(128))
    Image = db.Column(db.String(256))
    Price = db.Column(db.Float)
    Tags = db.Column(db.String(128))
    Discription = db.Column(db.String(256))
    def __repr__(self):
        return '<EflowerCombines{}>'.format(self.combineNumber)

class EflowerCombineOrders(db.Model):
    __tablename__ = 'EflowerCombineOrders'
    combineNumber = db.Column(db.String(64),db.ForeignKey('EflowerCombines.combineNumber'),primary_key=True)
    orderNumber = db.Column(db.String(64),db.ForeignKey('EOrders.orderNumber'),primary_key=True)
    buyQuantity = db.Column(db.Integer)
    def __repr__(self):
        return '<EflowerCombineOrders{}>'.format(self.orderNumber)

#--------------Message----------------
class MsgHistory(db.Model):
    Sender = db.Column(db.String(128),index=True)
    Message = db.Column(db.String(1024))
    print("==============")
    print(type(Sender))
    sendTime = db.Column(db.String(64),primary_key=True)
    Receiver = db.Column(db.String(128),index=True)
    def __repr__(self):
        return '<MsgHistory{}>'.format(self.Message)
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Admin(db.Model):
    adminNumber = db.Column(db.String(64),primary_key=True)
    adminPassword = db.Column(db.String(128))
    def __repr__(self):
        return '<Admin{}>'.format(self.adminNumber)

class ChangeFormat(db.Model):
    formatId = db.Column(db.Integer, primary_key=True)
    introduction = db.Column(db.String(1500))
    cv1 = db.Column(db.String(1500))
    cv2 = db.Column(db.String(1500))
    cv3 = db.Column(db.String(1500))
    def __repr__(self):
        return '<ChangeFormat{}>'.format(self.introduction)