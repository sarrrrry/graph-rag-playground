FROM neo4j:latest

ENV NEO4J_AUTH=neo4j/neo4j

# APOCプラグインをインストール
RUN wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.15.0/apoc-5.15.0-core.jar -P /var/lib/neo4j/plugins/

# Neo4jの設定を更新
RUN echo "dbms.security.procedures.unrestricted=apoc.*" >> /var/lib/neo4j/conf/neo4j.conf && \
    echo "apoc.import.file.enabled=true" >> /var/lib/neo4j/conf/neo4j.conf && \
    echo "apoc.import.file.use_neo4j_config=false" >> /var/lib/neo4j/conf/neo4j.conf

EXPOSE 7474 7687

CMD ["neo4j"]