--民國日期字串 → 西元 date
create or replace function parse_roc_date(p text)
returns date language sql immutable as $$
  select case
    when p ~ '^\d{2,3}[./]\d{1,2}[./]\d{1,2}$'
      then make_date(1911 + split_part(p, '[./]', 1)::int,
                     split_part(regexp_replace(p,'\.','/','g'), '/', 2)::int,
                     split_part(regexp_replace(p,'\.','/','g'), '/', 3)::int)
    else null
  end
$$;

-- 主表：projects
create table if not exists projects (
  id                bigserial primary key,
  project_code      text unique,          -- 計畫代碼
  project_name      text,                 -- 計畫名稱
  exec_unit         text,                 -- 執行單位
  fund_source       text,                 -- 經費來源(原文)
  unit_category     text,                 -- 單位(政府/企業/其他) ← 由AI/觸發器產出
  pi_code           text,                 -- 計畫主持人(代號)
  start_date        date,                 -- 起始日期
  end_date          date,                 -- 應結日期
  extend_date_raw   date,                 -- 延長日期(原樣保存，因常為「…」)
  close_date        date,                 -- 簽結日期(=實結日期)
  approve_amount    numeric,              -- 計畫核定數
  received_amount   numeric,              -- 實收數
  spent_amount      numeric,              -- 實支數
  refund_amount_raw text,                 -- 餘額繳回(常見為"-"，先原樣存)
  manage_fee        numeric,              -- 管理費
  created_at        timestamptz default now()
);

create index if not exists idx_projects_code on projects(project_code);
create index if not exists idx_projects_unit_category on projects(unit_category);
create index if not exists idx_projects_year on projects(extract(year from start_date));

-- 依執行單位(exec_unit)判別出的學院名稱
alter table projects
  add column if not exists college_category text;

-- 如果你會常用學院來 group by / 篩選，可以順便建 index
create index if not exists idx_projects_college_category
  on projects(college_category);

-- 對照表：執行單位關鍵字 → 學院名稱
create table if not exists college_map (
  id            bigserial primary key,
  unit_keyword  text        not null,          -- 執行單位中會出現的關鍵字，例如「電機」「資工」
  college_name  text        not null,          -- 學院名稱，例如「電機資訊學院」
  priority      int         not null default 100, -- 關鍵字優先順序，數字越小優先度越高
  created_at    timestamptz not null default now()
);

insert into college_map (unit_keyword, college_name, priority) values
-- 法律學院
('法律學院','法律學院',1),
('法律學系','法律學院',1),
('比較法資料中心','法律學院',1),

-- 商學院
('商學院','商學院',1),
('企業管理學系','商學院',1),
('金融與合作經營學系','商學院',1),
('會計學系','商學院',1),
('統計學系','商學院',1),
('休閒運動管理學系','商學院',1),
('資訊管理研究所','商學院',1),
('國際企業研究所','商學院',1),
('數位行銷進修學士學位學程','商學院',1),
('財務金融英語碩士學位學程','商學院',1),
('國際財務金融碩士在職專班','商學院',1),
('比較法資料中心','商學院',1),
('電子商務研究中心','商學院',1),
('企業永續中心','商學院',1),
('合作經濟暨非營利事業研究中心','商學院',1),
('金融科技暨綠色金融研究中心','商學院',1),

-- 公共事務學院
('公共事務學院','公共事務學院',1),
('公共行政暨政策學系','公共事務學院',1),
('財政學系','公共事務學院',1),
('不動產與城鄉環境學系','公共事務學院',1),
('都市計畫研究所','公共事務學院',1),
('自然資源與環境管理研究所','公共事務學院',1),
('民意與選舉研究中心','公共事務學院',1),
('土地與環境規劃研究中心','公共事務學院',1),

-- 社會科學學院
('社會科學學院','社會科學學院',1),
('經濟學系','社會科學學院',1),
('社會學系','社會科學學院',1),
('社會工作學系','社會科學學院',1),
('犯罪學研究所','社會科學學院',1),
('台灣青年發展與創新研究中心','社會科學學院',1),
('高齡與社區研究中心','社會科學學院',1),

-- 人文學院
('人文學院','人文學院',1),
('中國文學系','人文學院',1),
('應用外語學系','人文學院',1),
('歷史學系','人文學院',1),
('民俗藝術與文化資產研究所','人文學院',1),
('師資培育中心','人文學院',1),
('東西哲學與詮釋學研究中心','人文學院',1),

-- 電機資訊學院
('電機資訊學院','電機資訊學院',1),
('資訊工程學系','電機資訊學院',1),
('電機工程學系','電機資訊學院',1),
('通訊工程學系','電機資訊學院',1),
('智慧製造與系統應用產業碩士專班','電機資訊學院',1),
('電機資訊學院博士班','電機資訊學院',1),
('前瞻研究中心','電機資訊學院',1),

-- 永續創新國際學院
('永續創新國際學院','永續創新國際學院',1),
('城市治理英語碩士學位學程','永續創新國際學院',1),
('財務金融英語碩士學位學程','永續創新國際學院',1),
('智慧醫療管理英語碩士學位學程','永續創新國際學院',1),
('智慧永續發展與管理英語學士學位學程','永續創新國際學院',1),
('創新華語文教學學士學位學程','永續創新國際學院',1),
('華語中心','永續創新國際學院',1);