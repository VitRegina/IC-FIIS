-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.1.6
-- PostgreSQL version: 17.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
CREATE DATABASE new_database;
-- ddl-end --


-- object: public.fundo | type: TABLE --
-- DROP TABLE IF EXISTS public.fundo CASCADE;
CREATE TABLE public.fundo (
	id serial NOT NULL,
	codigo_fundo varchar(15),
	nome_fundo varchar(300),
	CONSTRAINT unique_codigo_fundo UNIQUE (codigo_fundo),
	CONSTRAINT fundo_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.fundo OWNER TO postgres;
-- ddl-end --

-- object: public.provento | type: TABLE --
-- DROP TABLE IF EXISTS public.provento CASCADE;
CREATE TABLE public.provento (
	id serial NOT NULL,
	fundo_id integer,
	valor_provento numeric(10,4),
	data_pagamento date,
	data_base date,
	periodo_referencia date,
	id_fundo integer,
	CONSTRAINT provento_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.provento OWNER TO postgres;
-- ddl-end --

-- object: fundo_fk | type: CONSTRAINT --
-- ALTER TABLE public.provento DROP CONSTRAINT IF EXISTS fundo_fk CASCADE;
ALTER TABLE public.provento ADD CONSTRAINT fundo_fk FOREIGN KEY (id_fundo)
REFERENCES public.fundo (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_provento_fundo | type: CONSTRAINT --
-- ALTER TABLE public.provento DROP CONSTRAINT IF EXISTS fk_provento_fundo CASCADE;
ALTER TABLE public.provento ADD CONSTRAINT fk_provento_fundo FOREIGN KEY (fundo_id)
REFERENCES public.fundo (id) MATCH SIMPLE
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


