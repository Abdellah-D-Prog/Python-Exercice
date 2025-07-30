--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: camps; Type: TABLE; Schema: public; Owner: scout
--

CREATE TABLE public.camps (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    location character varying(200) NOT NULL,
    duration_days integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.camps OWNER TO scout;

--
-- Name: camps_id_seq; Type: SEQUENCE; Schema: public; Owner: scout
--

CREATE SEQUENCE public.camps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.camps_id_seq OWNER TO scout;

--
-- Name: camps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scout
--

ALTER SEQUENCE public.camps_id_seq OWNED BY public.camps.id;


--
-- Name: scoots; Type: TABLE; Schema: public; Owner: scout
--

CREATE TABLE public.scoots (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    age integer NOT NULL,
    group_name character varying(100) NOT NULL,
    camp_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.scoots OWNER TO scout;

--
-- Name: scoots_id_seq; Type: SEQUENCE; Schema: public; Owner: scout
--

CREATE SEQUENCE public.scoots_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scoots_id_seq OWNER TO scout;

--
-- Name: scoots_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scout
--

ALTER SEQUENCE public.scoots_id_seq OWNED BY public.scoots.id;


--
-- Name: camps id; Type: DEFAULT; Schema: public; Owner: scout
--

ALTER TABLE ONLY public.camps ALTER COLUMN id SET DEFAULT nextval('public.camps_id_seq'::regclass);


--
-- Name: scoots id; Type: DEFAULT; Schema: public; Owner: scout
--

ALTER TABLE ONLY public.scoots ALTER COLUMN id SET DEFAULT nextval('public.scoots_id_seq'::regclass);


--
-- Data for Name: camps; Type: TABLE DATA; Schema: public; Owner: scout
--

COPY public.camps (id, name, location, duration_days, created_at) FROM stdin;
1	Camp d'été 2025	Chamonix	14	2025-07-30 00:40:49.581781
2	Weekend nature	Forêt de Fontainebleau	2	2025-07-30 00:40:49.581781
3	Camp hivernal	Les Gets	8	2025-07-30 00:40:49.581781
4	Camp aventure	Pyrénées	10	2025-07-30 00:40:49.581781
\.


--
-- Data for Name: scoots; Type: TABLE DATA; Schema: public; Owner: scout
--

COPY public.scoots (id, name, age, group_name, camp_id, created_at) FROM stdin;
1	Jean Dupont	15	Éclaireurs	1	2025-07-30 00:40:49.583171
2	Marie Martin	14	Guides	2	2025-07-30 00:40:49.583171
3	Paul Bernard	16	Routiers	1	2025-07-30 00:40:49.583171
4	Sophie Durand	13	Jeannettes	2	2025-07-30 00:40:49.583171
5	Lucas Moreau	17	Compagnons	3	2025-07-30 00:40:49.583171
6	Emma Petit	12	Louveteaux	\N	2025-07-30 00:40:49.583171
8	string	10	string	\N	2025-07-30 01:05:54.20721
9	strinzg	8	string	\N	2025-07-30 01:24:33.365682
10	string	9	string	\N	2025-07-30 01:30:55.959961
11	string	11	string	\N	2025-07-30 01:36:41.250339
\.


--
-- Name: camps_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scout
--

SELECT pg_catalog.setval('public.camps_id_seq', 4, true);


--
-- Name: scoots_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scout
--

SELECT pg_catalog.setval('public.scoots_id_seq', 11, true);


--
-- Name: camps camps_pkey; Type: CONSTRAINT; Schema: public; Owner: scout
--

ALTER TABLE ONLY public.camps
    ADD CONSTRAINT camps_pkey PRIMARY KEY (id);


--
-- Name: scoots scoots_pkey; Type: CONSTRAINT; Schema: public; Owner: scout
--

ALTER TABLE ONLY public.scoots
    ADD CONSTRAINT scoots_pkey PRIMARY KEY (id);


--
-- Name: scoots scoots_camp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: scout
--

ALTER TABLE ONLY public.scoots
    ADD CONSTRAINT scoots_camp_id_fkey FOREIGN KEY (camp_id) REFERENCES public.camps(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

