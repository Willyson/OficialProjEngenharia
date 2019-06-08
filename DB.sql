CREATE DATABASE DB_LOCALIZA;

-- =======================
-- TABELA TIPO_CONTA
-- =======================


CREATE TABLE IF NOT EXISTS `DB_LOCALIZA`.`TIPO_CONTA` 
(
  `ID_TIPO_CONTA` INT NOT NULL AUTO_INCREMENT,
  `DESC_TIPO_CONTA` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`ID_TIPO_CONTA`)
)
-- ======================
-- VALORES PADRÃO 
-- =====================

INSERT INTO TIPO_CONTA VALUES (1, 'Administrador'), (2, 'Comum');



-- =======================
-- TABELA USUARIO
-- =======================

CREATE TABLE IF NOT EXISTS `DB_LOCALIZA`.`USUARIO` (
  `ID_USUARIO` INT NOT NULL AUTO_INCREMENT,
  `CPF_USUARIO` VARCHAR(11) NOT NULL,
  `NOME_USUARIO` VARCHAR(250) NOT NULL,
  `RG_USUARIO` VARCHAR(9) NOT NULL,
  `EMAIL_USUARIO` VARCHAR(250) NULL,
  `SENHA_USUARIO` VARCHAR(500) NOT NULL,
  `STATUS_USUARIO` TINYINT(1) NOT NULL,
  `ID_TIPO_CONTA` INT NOT NULL,
  PRIMARY KEY (`ID_USUARIO`),
    FOREIGN KEY (`ID_TIPO_CONTA`) REFERENCES `DB_LOCALIZA`.`TIPO_CONTA` (`ID_TIPO_CONTA`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)

-- ======================
-- VALORES PADRÃO 
-- =====================
INSERT INTO USUARIO
(
	 CPF_USUARIO 
	,NOME_USUARIO
	,RG_USUARIO
	,EMAIL_USUARIO
	,SENHA_USUARIO
	,STATUS_USUARIO
	,ID_TIPO_CONTA
) 
VALUES ('12345678910', 'Admin', '12345567','admin@email.com','1234','1','1');





-- ======================
-- TABELA TORRE_SITE 
-- =====================

CREATE TABLE IF NOT EXISTS `DB_LOCALIZA`.`TORRE_SITE` (
  `ID_TORRE` VARCHAR(8) NOT NULL,
  `ALT_TORRE` FLOAT NOT NULL,
  `LATIT_TORRE` FLOAT NOT NULL,
  `LOGIT_TORRE` FLOAT NOT NULL,
  PRIMARY KEY (`ID_TORRE`))




-- ======================
-- TABELA ENDERECO 
-- =====================

CREATE TABLE IF NOT EXISTS `DB_LOCALIZA`.`ENDERECO` (
  `ID_ENDERECO`     INT NOT NULL AUTO_INCREMENT,
  `CEP_ENDERECO`    INT  NULL,
  `BAIRRO_ENDERECO` VARCHAR(250)  NULL,
  `CIDADE_ENDERECO` VARCHAR(250)  NULL,
  `UF_ENDERECO`     CHAR(2) NULL,
  `ID_USUARIO`      INT NULL,
  `ID_TORRE`        VARCHAR(8) NULL,
  PRIMARY KEY (`ID_ENDERECO`),
  CONSTRAINT `fk_ENDERECO_USUARIO1`     FOREIGN KEY (`ID_USUARIO`) REFERENCES `DB_LOCALIZA`.`USUARIO` (`ID_USUARIO`),
  CONSTRAINT `fk_ENDERECO_TORRE_SITE`   FOREIGN KEY (`ID_TORRE`)   REFERENCES `DB_LOCALIZA`.`TORRE_SITE` (`ID_TORRE`))



-- =====================================================
-- VALORES PADRÃO PARA A TORRE_SITE COMO PARA O ENDERECO
-- ======================================================

INSERT INTO TORRE_SITE VALUES('SPFRC007', '34', '-20.5055', '-47.401417');
INSERT INTO ENDERECO (UF_ENDERECO, CIDADE_ENDERECO, ID_TORRE, ID_USUARIO) VALUES ('SP','FRANCA', 'SPFRC007','1');

INSERT INTO TORRE_SITE VALUES('SPFRC012', '20', '-20.5208', '-47.4085');
INSERT INTO ENDERECO (UF_ENDERECO, CIDADE_ENDERECO, ID_TORRE, ID_USUARIO) VALUES ('SP','FRANCA', 'SPFRC012','1');

INSERT INTO TORRE_SITE VALUES('SPFRC021', '30', '-20.5257', '-47.365962');
INSERT INTO ENDERECO (UF_ENDERECO, CIDADE_ENDERECO, ID_TORRE, ID_USUARIO) VALUES ('SP','FRANCA', 'SPFRC021','1');


INSERT INTO TORRE_SITE VALUES('SPFRC035', '24', '-20.5786', '-47.3806');
INSERT INTO ENDERECO (UF_ENDERECO, CIDADE_ENDERECO, ID_TORRE, ID_USUARIO) VALUES ('SP','FRANCA', 'SPFRC035','1');


-- ======================
-- TABELA ANTENA_SETOR 
-- =====================

CREATE TABLE IF NOT EXISTS `DB_LOCALIZA`.`ANTENA_SETOR` (
  `ID_ANTENA` VARCHAR(9) NOT NULL,
  `AZIMUTE_ANTENA` INT NOT NULL,
  `MECHANICAL_TITL_ANTENA` INT NOT NULL,
  `HORIZONTAL_BW_ANTENA` INT NOT NULL,
  `VERTICAL_BW_ANTENA` INT NOT NULL,
  `STATUS_ANTENA` TINYINT(1) NOT NULL,
  `DESC_ANTENA` VARCHAR(500) NULL,
  `ID_TORRE` VARCHAR(8) NOT NULL,
  PRIMARY KEY (`ID_ANTENA`),
  CONSTRAINT `fk_ANTENA_SETOR_TORRE_SITE1`  FOREIGN KEY (`ID_TORRE`)  REFERENCES `DB_LOCALIZA`.`TORRE_SITE` (`ID_TORRE`));

INSERT INTO ANTENA_SETOR VALUES 
('SPFRC0071', '320', '3', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC007'),
('SPFRC0072', '80',  '3', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC007'),
('SPFRC0073', '200', '8', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC007');

INSERT INTO ANTENA_SETOR VALUES 
('SPFRC0121', '330', '5', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC012'),
('SPFRC0122', '80',  '5', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC012'),
('SPFRC0123', '190', '3', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC012');

INSERT INTO ANTENA_SETOR VALUES 
('SPFRC0211', '340', '3', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC021'),
('SPFRC0212', '70',  '3', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC021'),
('SPFRC0213', '205', '3', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC021');

INSERT INTO ANTENA_SETOR VALUES
('SPFRC0351', '85', '3', '65', '5', '1', 'ANTENA PADRÃO', 'SPFRC035'),
('SPFRC0352', '230', '3', '65', '5','1', 'ANTENA PADRÃO', 'SPFRC035'),
('SPFRC0353', '310', '3', '65', '5','1', 'ANTENA PADRÃO', 'SPFRC035');


CREATE VIEW V_CONSULTA_TORRE_ANTENA AS 
SELECT 
	 TS.ID_TORRE   AS 'ID DA TORRE'
    ,LOGIT_TORRE   AS 'LONGITUDE'
    ,LATIT_TORRE   AS 'LATITUDE'
    ,ALT_TORRE     AS 'ALTURA'
    ,ANS.ID_ANTENA AS 'ID DA ANTENA'
    ,ANS.AZIMUTE_ANTENA AS 'AZIMUTH'
    ,ANS.MECHANICAL_TITL_ANTENA AS 'MECHANICAL'
    ,ANS.HORIZONTAL_BW_ANTENA AS 'HORIZONTAL'
    ,ANS.VERTICAL_BW_ANTENA AS 'VERTICAL'
    ,E.CIDADE_ENDERECO AS 'ENDERECO'
    ,E.UF_ENDERECO AS 'UF'
    ,ANS.STATUS_ANTENA AS 'STATUS'
FROM TORRE_SITE TS 
INNER JOIN ANTENA_SETOR ANS ON (TS.ID_TORRE = ANS.ID_TORRE) 
INNER JOIN ENDERECO E ON (E.ID_TORRE = TS.ID_TORRE)
ORDER BY ANS.STATUS_ANTENA, TS.ID_TORRE



 -- =========================================
 -- Estrutura de Log de consulta de endereço
 -- =========================================

 CREATE TABLE IF NOT EXISTS `DB_LOCALIZA`.`LOG_CONSULTA_ENDERECO`
 (
   `ID_LOG` INT NOT NULL AUTO_INCREMENT, 
   `LOCALIZACAO` VARCHAR(250) NULL, 
   `RETORNO` TINYINT NULL, 
   `DATA_CONSULTA` DATETIME NULL,
   PRIMARY KEY (ID_LOG)

 )
 
 
 
 
CREATE VIEW VW_CONSULTA_ENDERECO
AS
SELECT 
     LOCALIZACAO 
    ,CASE 
        WHEN RETORNO = 1 THEN 'ENDEREÇO VÁLIDO'
        WHEN RETORNO = 0 THEN 'ENDEREÇO NÃO VÁLIDO'
        ELSE ''
    END AS RETORNO
    ,DATE_FORMAT(DATA_CONSULTA, '%d/%m/%Y %H:%i:%s') AS DATA_CONSULTA
FROM LOG_CONSULTA_ENDERECO
ORDER BY DATA_CONSULTA DESC;


CREATE VIEW VW_SELECIONA_USUARIO AS 
SELECT 
     ID_USUARIO
    ,CPF_USUARIO
    ,NOME_USUARIO
    ,EMAIL_USUARIO
    ,SENHA_USUARIO
    ,STATUS_USUARIO
    ,TC.DESC_TIPO_CONTA
FROM USUARIO U 
INNER JOIN TIPO_CONTA TC ON (U.ID_TIPO_CONTA = TC.ID_TIPO_CONTA);

 