from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent/'labs'
def write(name,items):
 p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(yaml.safe_dump_all(items,sort_keys=False) if isinstance(items,list) else items)
def pod(name,container,**spec):return dict(apiVersion='v1',kind='Pod',metadata=dict(name=name,namespace='tk-bank'),spec=dict(containers=[container],**spec))
ns={'apiVersion':'v1','kind':'Namespace','metadata':{'name':'tk-bank'}}
cm={'apiVersion':'v1','kind':'ConfigMap','metadata':{'name':'bank-page','namespace':'tk-bank'},'data':{'index.html':'<!doctype html><html><h1>Harbour Bank learning service</h1><p>Version one. Fictional information only.</p></html>'}}
container={'name':'web','image':'nginx:1.27-alpine','ports':[{'containerPort':80}],'resources':{'requests':{'cpu':'50m','memory':'32Mi'},'limits':{'cpu':'250m','memory':'128Mi'}},'readinessProbe':{'httpGet':{'path':'/','port':80},'periodSeconds':3},'livenessProbe':{'httpGet':{'path':'/','port':80},'initialDelaySeconds':10,'periodSeconds':10},'volumeMounts':[{'name':'page','mountPath':'/usr/share/nginx/html','readOnly':True}]}
dep={'apiVersion':'apps/v1','kind':'Deployment','metadata':{'name':'bank-web','namespace':'tk-bank'},'spec':{'replicas':2,'selector':{'matchLabels':{'app':'bank-web'}},'strategy':{'type':'RollingUpdate','rollingUpdate':{'maxUnavailable':0,'maxSurge':1}},'template':{'metadata':{'labels':{'app':'bank-web'}},'spec':{'automountServiceAccountToken':False,'containers':[container],'volumes':[{'name':'page','configMap':{'name':'bank-page'}}]}}}}
svc={'apiVersion':'v1','kind':'Service','metadata':{'name':'bank-web','namespace':'tk-bank'},'spec':{'selector':{'app':'bank-web'},'ports':[{'port':80,'targetPort':80}]}}
write('bank.yaml',[ns,cm,dep,svc])
write('init.yaml',[pod('bank-init',{'name':'web','image':'nginx:1.27-alpine','volumeMounts':[{'name':'shared','mountPath':'/usr/share/nginx/html'}]},initContainers=[{'name':'prepare','image':'busybox:1.37','command':['sh','-c','echo "Harbour Bank prepared page" > /work/index.html'],'volumeMounts':[{'name':'shared','mountPath':'/work'}]}],volumes=[{'name':'shared','emptyDir':{}}])])
jobSpec={'backoffLimit':1,'template':{'spec':{'restartPolicy':'Never','containers':[{'name':'report','image':'busybox:1.37','command':['sh','-c','echo "Fictional bank report: total demo units 3500"']}]}}}
write('jobs.yaml',[{'apiVersion':'batch/v1','kind':'Job','metadata':{'name':'bank-report','namespace':'tk-bank'},'spec':jobSpec},{'apiVersion':'batch/v1','kind':'CronJob','metadata':{'name':'bank-report-schedule','namespace':'tk-bank'},'spec':{'schedule':'0 6 * * *','timeZone':'Etc/UTC','suspend':True,'concurrencyPolicy':'Forbid','successfulJobsHistoryLimit':1,'failedJobsHistoryLimit':1,'jobTemplate':{'spec':jobSpec}}}])
write('secret-reader.yaml',[{'apiVersion':'v1','kind':'Secret','metadata':{'name':'dummy-report','namespace':'tk-bank'},'type':'Opaque','stringData':{'token':'fictional-training-token'}},pod('secret-reader',{'name':'reader','image':'busybox:1.37','command':['sh','-c','wc -c < /secret/token'],'volumeMounts':[{'name':'secret','mountPath':'/secret','readOnly':True}]},restartPolicy='Never',automountServiceAccountToken=False,volumes=[{'name':'secret','secret':{'secretName':'dummy-report'}}])])
write('pending.yaml',[pod('bank-pending',{'name':'worker','image':'busybox:1.37','command':['sleep','3600'],'resources':{'requests':{'cpu':'100','memory':'32Mi'}}})])
write('rbac.yaml',[{'apiVersion':'v1','kind':'ServiceAccount','metadata':{'name':'bank-reader','namespace':'tk-bank'}},{'apiVersion':'rbac.authorization.k8s.io/v1','kind':'Role','metadata':{'name':'bank-pod-reader','namespace':'tk-bank'},'rules':[{'apiGroups':[''],'resources':['pods'],'verbs':['get','list','watch']}]},{'apiVersion':'rbac.authorization.k8s.io/v1','kind':'RoleBinding','metadata':{'name':'bank-pod-reader','namespace':'tk-bank'},'subjects':[{'kind':'ServiceAccount','name':'bank-reader','namespace':'tk-bank'}],'roleRef':{'apiGroup':'rbac.authorization.k8s.io','kind':'Role','name':'bank-pod-reader'}}])
write('security.yaml',[pod('secure-worker',{'name':'worker','image':'busybox:1.37','command':['sh','-c','id; echo safe > /work/result; cat /work/result; sleep 3600'],'securityContext':{'allowPrivilegeEscalation':False,'readOnlyRootFilesystem':True,'capabilities':{'drop':['ALL']}},'volumeMounts':[{'name':'work','mountPath':'/work'}]},automountServiceAccountToken=False,securityContext={'runAsNonRoot':True,'runAsUser':10001,'runAsGroup':10001,'fsGroup':10001,'seccompProfile':{'type':'RuntimeDefault'}},volumes=[{'name':'work','emptyDir':{}}])])
write('storage.yaml',[{'apiVersion':'v1','kind':'PersistentVolumeClaim','metadata':{'name':'bank-learning-data','namespace':'tk-bank'},'spec':{'accessModes':['ReadWriteOnce'],'resources':{'requests':{'storage':'128Mi'}}}},pod('bank-storage',{'name':'worker','image':'busybox:1.37','command':['sleep','3600'],'volumeMounts':[{'name':'data','mountPath':'/data'}]},volumes=[{'name':'data','persistentVolumeClaim':{'claimName':'bank-learning-data'}}])])
write('policy.yaml',[{'apiVersion':'networking.k8s.io/v1','kind':'NetworkPolicy','metadata':{'name':'bank-web-ingress','namespace':'tk-bank'},'spec':{'podSelector':{'matchLabels':{'app':'bank-web'}},'policyTypes':['Ingress'],'ingress':[{'from':[{'podSelector':{'matchLabels':{'role':'frontend'}}}],'ports':[{'protocol':'TCP','port':80}]}]}}])
write('ingress.yaml',[{'apiVersion':'networking.k8s.io/v1','kind':'Ingress','metadata':{'name':'bank-web','namespace':'tk-bank'},'spec':{'ingressClassName':'replace-with-installed-class','rules':[{'host':'bank.example.test','http':{'paths':[{'path':'/','pathType':'Prefix','backend':{'service':{'name':'bank-web','port':{'number':80}}}}]}}]}}])
write('reports-crd.yaml',[{'apiVersion':'apiextensions.k8s.io/v1','kind':'CustomResourceDefinition','metadata':{'name':'bankreports.learning.techknowen.example'},'spec':{'group':'learning.techknowen.example','scope':'Namespaced','names':{'plural':'bankreports','singular':'bankreport','kind':'BankReport','shortNames':['brpt']},'versions':[{'name':'v1','served':True,'storage':True,'schema':{'openAPIV3Schema':{'type':'object','properties':{'spec':{'type':'object','required':['period'],'properties':{'period':{'type':'string','pattern':'^[0-9]{4}-[0-9]{2}$'}}}}}}}]}}])
write('report.yaml',[{'apiVersion':'learning.techknowen.example/v1','kind':'BankReport','metadata':{'name':'september','namespace':'tk-bank'},'spec':{'period':'2026-09'}}])
write('bank-info/Chart.yaml','apiVersion: v2\nname: bank-info\ndescription: Original TechKnowen teaching chart\ntype: application\nversion: 0.1.0\nappVersion: "1.27"\n')
write('bank-info/values.yaml','replicaCount: 2\nimage: nginx:1.27-alpine\n')
write('bank-info/templates/deployment.yaml','''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app.kubernetes.io/instance: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app.kubernetes.io/instance: {{ .Release.Name }}
    spec:
      containers:
        - name: web
          image: {{ .Values.image | quote }}
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
---
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}
spec:
  selector:
    app.kubernetes.io/instance: {{ .Release.Name }}
  ports:
    - port: 80
      targetPort: 80
''')
write('kustomize/base/kustomization.yaml','resources:\n  - deployment.yaml\n')
write('kustomize/base/deployment.yaml',[{'apiVersion':'apps/v1','kind':'Deployment','metadata':{'name':'bank-overlay'},'spec':{'replicas':2,'selector':{'matchLabels':{'app':'bank-overlay'}},'template':{'metadata':{'labels':{'app':'bank-overlay'}},'spec':{'containers':[{'name':'web','image':'nginx:1.27-alpine'}]}}}}])
write('kustomize/overlays/practice/kustomization.yaml','resources:\n  - ../../base\n  - namespace.yaml\nnamespace: tk-kustomize\nreplicas:\n  - name: bank-overlay\n    count: 3\n')
write('kustomize/overlays/practice/namespace.yaml',[{'apiVersion':'v1','kind':'Namespace','metadata':{'name':'tk-kustomize'}}])
