# Textos de las secciones corporativas de la portada (globaltni.com/en, medidos el 3-nov-2026; ver docs/design/oficinas/corporativas-globaltni.md).
# Son de Truly Nolen International, no de la oficina: la base es el español con tú (VE, NI; clave del texto en el generador), y cada ficha
# lleva su versión en `textos`: Panamá en usted (es el texto oficial de globaltni.com/es) y Francia en francés (traducción fiel del inglés).
# `python scripts/corporativas_textos.py` escribe esas entradas en app/src/inbound/oficinas/{panama,francia}.json (no toca las demás claves).
# Cada fila: (español con tú = clave, español de usted [None si es igual], francés)
import json,sys
from pathlib import Path
T=[
 # Saneamiento
 ('Virus, hongos y bacterias',None,'Virus, champignons et bactéries'),
 ('Sanitización de ambientes interiores.',None,'Assainissement des environnements intérieurs.'),
 ('La sanitización reúne estrategias para prevenir y controlar la contaminación por virus, hongos y bacterias, según el tipo de ambiente interior.',None,'L’assainissement regroupe des stratégies pour prévenir et maîtriser la contamination par des virus, des champignons et des bactéries, selon le type d’environnement intérieur.'),
 ('Conoce el servicio de sanitización →','Conozca el servicio de sanitización →','Découvrir le service d’assainissement →'),
 ('Un protocolo según el ambiente.',None,'Un protocole adapté à chaque environnement.'),
 ('Entrevista e identificación del entorno. Selección de producto, aplicación y tiempo de contacto. Medidas de prevención y control para cada instalación.',None,'Comprendre l’environnement. Choisir le produit, l’application et le temps de contact. Définir les mesures de prévention et de contrôle de l’installation.'),
 # TEPS
 ('Truly Elite Protection System',None,'Truly Elite Protection System'),
 ('TEPS: un programa con seguimiento.',None,'TEPS : un programme avec un suivi continu.'),
 ('Inspección, plan de control, registro de cada visita y revisión de tendencias. Un programa de Manejo Integrado de Plagas con trazabilidad y estándares auditados.',None,'Inspection, plan de contrôle, registre de chaque visite et revue des tendances. Un programme de lutte intégrée contre les nuisibles, avec traçabilité et normes auditées.'),
 ('Explora el sistema TEPS →','Explore el sistema TEPS →','Découvrir le programme TEPS →'),
 ('Inspeccionar',None,'Inspecter'),
 ('Evaluamos la instalación y su entorno',None,'Nous évaluons l’installation et son environnement'),
 ('Identificamos actividad de plagas, puntos de acceso, condiciones favorables y prácticas operativas para determinar las necesidades del programa.',None,'Nous repérons l’activité des nuisibles, les points d’accès, les conditions favorables et les pratiques d’exploitation pour déterminer les besoins du programme.'),
 ('Desarrollar el programa',None,'Élaborer le programme'),
 ('Un plan específico para la instalación',None,'Un plan propre à l’installation'),
 ('El entorno, la estacionalidad, la actividad observada, las prácticas de operación y las plagas identificadas determinan el programa.',None,'L’environnement, la saisonnalité, l’activité observée, les pratiques d’exploitation et les nuisibles identifiés déterminent le programme.'),
 ('Registrar cada visita',None,'Consigner chaque visite'),
 ('El trabajo queda documentado',None,'Le travail est documenté'),
 ('Después de cada servicio, el técnico registra las actividades realizadas y los hallazgos identificados en la instalación.',None,'Après chaque intervention, le technicien consigne les actions réalisées et les constats relevés dans l’installation.'),
 ('Revisar las tendencias',None,'Examiner les tendances'),
 ('Informes mensuales y recomendaciones',None,'Rapports mensuels et recommandations'),
 ('Los datos registrados sobre la actividad de plagas permiten analizar tendencias y dar seguimiento a las acciones.',None,'Les données enregistrées sur l’activité des nuisibles permettent d’analyser les tendances et de suivre les actions.'),
 ('Formación, supervisión y respuesta durante el programa',None,'Formation, supervision et réponse tout au long du programme'),
 ('Capacitación personalizada',None,'Formation sur mesure'),
 ('Formación para clientes y empleados, con el respaldo del equipo técnico internacional.',None,'Formation des clients et des employés, avec l’appui de l’équipe technique internationale.'),
 ('Centro de formación virtual',None,'Centre de formation virtuel'),
 ('Capacitación a distancia para profundizar en los conocimientos del programa y sus protocolos.',None,'Formation à distance pour approfondir la connaissance du programme et de ses protocoles.'),
 ('Supervisión de calidad',None,'Assurance qualité'),
 ('Informe de auditoría y lista de verificación específica para el tipo de establecimiento, con un indicador de rendimiento.',None,'Un rapport d’audit et une liste de contrôle propres au type d’établissement, avec un indicateur de performance.'),
 ('Educación para el cliente',None,'Formation du client'),
 ('Formación sobre manejo integrado de plagas, biología, ecología, aspectos regulatorios y soporte de auditoría.',None,'Formation à la lutte intégrée, à la biologie, à l’écologie, à la réglementation et accompagnement pour les audits.'),
 ('Protocolos específicos',None,'Protocoles de service'),
 ('Programas personalizados para las necesidades de cada cliente, especialmente instalaciones auditadas.',None,'Des programmes adaptés aux besoins de chaque client, en particulier les installations auditées.'),
 ('Respuesta y seguimiento',None,'Réponse et suivi'),
 ('Se definen umbrales de acción con la administración. Si se superan, se aplica un protocolo de escalamiento hasta establecer el control.',None,'Les seuils d’action sont définis avec la direction de l’installation. S’ils sont dépassés, un protocole d’escalade est appliqué jusqu’au rétablissement du contrôle.'),
 # Red internacional
 ('Una red internacional',None,'Un réseau international'),
 ('Una red internacional. Atención en tu localidad.','Una red internacional. Atención en su localidad.','Une expertise internationale. Un service près de chez vous.'),
 ('Busca tu localidad en el directorio internacional. La oficina que atiende tu zona te ayudará a conocer el servicio y el programa adecuado para tu espacio.','Busque su localidad en el directorio internacional. La oficina que atiende su zona le ayudará a conocer el servicio y el programa adecuado para su espacio.','Trouvez votre localité dans notre annuaire international. Votre bureau local peut vous aider à comprendre le service et le programme adaptés à votre bien.'),
 ('Abrir el directorio de oficinas →',None,'Ouvrir l’annuaire des bureaux →'),
 ('Escríbenos desde el formulario de contacto →','Escríbanos desde el formulario de contacto →','Écrivez-nous via le formulaire de contact →'),
 ('La confianza de marcas reconocidas en todo el mundo.',None,'La confiance de marques reconnues dans le monde entier.'),
 ('Trabajamos con hogares y empresas a través de nuestra red internacional de oficinas.',None,'Nous travaillons avec des particuliers et des entreprises grâce à notre réseau international de bureaux.'),
 ('Conecta con una oficina local.','Conecte con una oficina local.','Contactez un bureau local.'),
 ('Accesos a sitios locales del directorio internacional.',None,'Sites locaux répertoriés dans notre annuaire international.'),
 ('Américas',None,'Amériques'),('Europa',None,'Europe'),('Asia',None,'Asie'),
 ('Argentina',None,'Argentine'),('Brasil',None,'Brésil'),('España',None,'Espagne'),('Francia',None,'France'),('India',None,'Inde'),('Filipinas',None,'Philippines'),
 ('Ver todos los países y contactos →',None,'Voir tous les pays et contacts →'),
 ('Alcance internacional',None,'Portée internationale'),
 ('continentes',None,'continents'),
 # Franquicias
 ('Franquicias Truly Nolen International',None,'Franchise Truly Nolen International'),
 ('Tu franquicia de control de plagas.','Su franquicia de control de plagas.','Votre franchise de lutte contre les nuisibles.'),
 ('Desarrolla un negocio con formación permanente en Manejo Integrado de Plagas, protocolos de servicio y soporte internacional.','Desarrolle un negocio con formación permanente en Manejo Integrado de Plagas, protocolos de servicio y soporte internacional.','Développez une activité avec une formation continue à la lutte intégrée, des protocoles de service et un soutien international.'),
 ('Formación que continúa después de la apertura.',None,'La formation continue après l’ouverture.'),
 ('El aprendizaje combina conocimientos técnicos y trabajo de campo. Los equipos estudian la biología de las plagas, practican la identificación y aprenden a aplicar los protocolos del servicio.',None,'La formation associe connaissances techniques et travail de terrain. Les équipes étudient la biologie des nuisibles, s’exercent à l’identification et apprennent à appliquer les protocoles de service.'),
 ('Formación continua',None,'Formation continue'),
 ('La formación comienza online con especialistas de Truly Nolen International y continúa con unos 10 días de práctica en tu país.','La formación comienza online con especialistas de Truly Nolen International y continúa con unos 10 días de práctica en su país.','La formation débute en ligne avec les spécialistes de Truly Nolen International et se poursuit par environ 10 jours de pratique dans votre pays.'),
 ('Soporte internacional',None,'Soutien international'),
 ('El equipo técnico internacional acompaña el aprendizaje y el desarrollo de protocolos.',None,'L’équipe technique internationale accompagne l’apprentissage et l’élaboration des protocoles.'),
 ('Un sistema de servicio compartido',None,'Un système de service partagé'),
 ('Manejo Integrado de Plagas, protocolo de tres zonas y los cinco pasos de Truly Care.',None,'La lutte intégrée, le protocole en trois zones et les cinq étapes de Truly Care.'),
 ('Quiero ser franquiciado →',None,'Je veux devenir franchisé →'),
 ('Conoce el modelo de franquicia →','Conozca el modelo de franquicia →','Découvrir le modèle de franchise →'),
 # Historia
 ('Más de 80 años de experiencia',None,'Plus de 80 ans d’expérience'),
 ('Prevenir las plagas. Una idea desde 1938.',None,'Prévenir les nuisibles. Une idée née en 1938.'),
 ('En 1938, Truly Wheatfield Nolen propuso proteger los edificios sellando las entradas de los roedores. La prevención estaba en el origen.',None,'En 1938, Truly Wheatfield Nolen proposait de protéger les bâtiments en bouchant les points d’entrée des rongeurs. La prévention était là dès l’origine.'),
 ('Hoy, esa visión se expresa en formación, métodos de control y protocolos diseñados para reducir el impacto en el entorno.',None,'Aujourd’hui, cette approche se prolonge par la formation, des méthodes de lutte et des protocoles conçus pour réduire l’impact sur l’environnement.'),
 ('Nuestra historia hasta ahora →',None,'Notre histoire jusqu’ici →'),
 ('Conoce a nuestro equipo →','Conozca a nuestro equipo →','Rencontrer notre équipe →'),
 ('Una idea centrada en la prevención.',None,'Une idée centrée sur la prévention.'),
 ('La visión llega a Argentina.',None,'La vision arrive en Argentine.'),
 ('Nace Truly Nolen International.',None,'Naissance de Truly Nolen International.'),
 # Índice «Un programa para su espacio» (globaltni.com/es y /en, 3-nov-2026; el francés es traducción fiel del inglés)
 ('Un programa para tu espacio.','Un programa para su espacio.','Un programme pour votre espace.'),
 ('De la inspección de una vivienda a los registros de una instalación auditada. Elige el servicio que necesitas conocer.','De la inspección de una vivienda a los registros de una instalación auditada. Elija el servicio que necesita conocer.','De l’inspection d’un logement à la documentation d’un programme pour une installation auditée. Trouvez le service qui répond à vos besoins.'),
 ('Monitoreo y control auditado',None,'Suivi et contrôle audités'),
 ('TEPS',None,'TEPS'),
 ('Estándares globales, seguimiento y reportes.',None,'Normes mondiales, suivi et rapports.'),
 ('Programas según tu sector y actividad.','Programas según su sector y actividad.','Des programmes adaptés à votre secteur et à votre activité.'),
 ('Comercial',None,'Commercial'),
 ('Inspección y cuidado en tres zonas.',None,'Inspection et soins dans trois zones.'),
 ('Residencial',None,'Résidentiel'),
 ('Control microbiano en interiores.',None,'Contrôle microbien en intérieur.'),
 ('Sanitización',None,'Assainissement'),
 ('El automóvil amarillo con orejas de ratón de Truly Nolen',None,'La voiture jaune aux oreilles de souris de Truly Nolen'),
 # Hero y fuentes
 ('Programa TEPS',None,'Programme TEPS'),
]
RAIZ=Path(__file__).resolve().parents[1]/'app/src/inbound/oficinas'
if __name__=='__main__':
    for oid,idx in (('panama',1),('francia',2)):
        p=RAIZ/f'{oid}.json';raw=p.read_text(encoding='utf-8');o=json.loads(raw)
        for fila in T:
            v=fila[idx]
            if v is not None and (idx==2 or v!=fila[0]):o['textos'][fila[0]]=v
            elif idx==1:continue
            elif v is None:continue
        p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(oid,'textos:',len(o['textos']))
