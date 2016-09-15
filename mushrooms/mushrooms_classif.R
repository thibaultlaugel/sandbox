library(DMwR)
library(class)
library (pROC)
library(ROCR)
library(rpart)
library(nnet)

###import database
#file = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Apprentissage/tp4/agaricus-lepiota.txt'
file = '//paradis/eleves/TLaugel/Bureau/TP Apprentissage/TP4/files/Mushrooms-classification-master/agaricus-lepiota.txt'
data = read.table(file, sep=',')







###############################################
# Preliminary work
###############################################


###clean database
#names
names(data)=c("edible","cap-shape","cap-surface","cap-color","bruises","odor","gill-attachment","gill-spacing","gill-size","gill-color","stalk-shape","stalk-root","stalk-surface-above-ring","stalk-surface-below-ring","stalk-color-above-ring","stalk-color-above-ring","veil-type","veil-color","ring-number","ring-type","spore-sprint-color","population","habitat")


#drop useless columns (only one value)
data=data[,-17]
head(data[,2])
#fill NA
#data_completed = knnImputation(data, k = 10)
#data_completed = na.omit(data)


#transform factor variables in dummies
data1=model.matrix(~data_completed[,1],data=data_completed)[,2:ncol(model.matrix(~data_completed[,1],data=data_completed))]
attributes = c("edible")
for(i in 2:ncol(data_completed))
{
	data1=cbind(data1,model.matrix(~data_completed[,i],data=data_completed)[,2:ncol(model.matrix(~data_completed[,i],data=data_completed))])
	varname = names(data)[i]
	n=length(lvl<-levels(data_completed[,i]))
	for (k in 2:n){
		modname=paste(varname,lvl[k],sep="_")
		attributes = cbind(attributes, modname)}
}
data1=as.data.frame(data1)
names(data1)=attributes



###Split train-test
N=length(data1[,1])
set.seed(42)
Index=sample(1:N)
K=round(0.7*N)
data.train=data1[Index[1:K],]
data.test=data1[Index[(K+1):N],]





###############################################
# Descriptive statistics
###############################################

head(data)
help(chisq.test)
matr=matrix(0,length(data),length(data))
for(j in 1:length(data))
for (i in 1:length(data)){
	khi2=chisq.test(data[,j],data[,i])[3]
	print(j); print(i)
	matr[j,i]=khi2}

table(data[,1],data[,"odor"])
table(data[,1],data[,"stalk-root"])





###############################################
# Classification models
###############################################
length(data.train)


###KNN

# 11-fold cross-validation to select k
set.seed(42)
kmax=30
kmin=1
fold = sample(rep(1:11,each=517))
cvpred = matrix(NA,nrow=5687,ncol=kmax)
for (k in kmin:kmax)
for (v in 1:11)
{
sample1 = data.train[which(fold!=v),2:95]
sample2 = data.train[which(fold==v),2:95]
class1 = data.train[which(fold!=v),1]
cvpred[which(fold==v),k] = knn(sample1,sample2,class1,k=k)
}
class = as.numeric(data.train[,1])
# display misclassification rates for k=kmin:kmax
a = apply(cvpred,2,function(x) sum(class!=x)) 
plot(a)
a
#k=10

#knn on test
set.seed(42)
ptm=proc.time()
pred = as.numeric(knn(data.train[,2:95], data.test[,2:95], 
data.train[,1], k = 10, prob=FALSE))
proc.time()-ptm

#confusion matrix
conf=as.matrix(table(pred,data.test[,1]))
sum(diag(conf))/sum(conf)

#plot roc
ROC=roc(data.test[,1],pred)
plot.roc(ROC,print.auc=TRUE, col="red", print.thresh="all")
#plot(performance(prediction(pred,data.test[,1]),measure="acc"))







###decision tree
rt.shrooms = rpart(as.factor(data.train[,1]) ~. , data = data.train[,-1])
pred.rt =predict(rt.shrooms, data.test[,-1], type="class")

#conf mat, acc
conf.rt=as.matrix(table(pred.rt,data.test[,1]))
sum(diag(conf.rt))/sum(conf.rt)

#plot tree
par(lwd=2, col="red")
plot(rt.shrooms, compress=TRUE)
text(rt.shrooms, use.n=TRUE,col="blue")

#roc
ROC=roc(data.test[,1],as.numeric(pred.rt))
plot.roc(ROC,print.auc=TRUE, col="red", print.thresh="all")
