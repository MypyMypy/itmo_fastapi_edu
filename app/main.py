from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from app.models import Base, engine
from app.schemas import TermCreate, TermResponse
from sqlalchemy.orm import Session
from app.crud import get_all_terms, create_term, get_term_by_name, update_term, delete_term

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    initial_terms = [
        {
            "name": "Веб-приложение",
            "description": "Программное приложение, использующее браузер в качестве клиентской среды и выполняющее бизнес-логику посредством сетевого взаимодействия с сервером.",
            "link": "https://sibdev.pro/blog/articles/chto-takoe-veb-prilozhenie"
        },
        {
            "name": "Клиент-серверная архитектура",
            "description": "Модель распределённой системы, предполагающая разделение компонентов на клиент, запрашивающий ресурсы, и сервер, обрабатывающий запросы.",
            "link": None
        },
        {
            "name": "Front-end",
            "description": "Часть веб-приложения, обеспечивающая отображение данных и взаимодействие пользователя с системой через браузер.",
            "link": "https://practicum.yandex.ru/blog/chem-otlichaetsya-backend-i-frontend/"
        },
        {
            "name": "Back-end",
            "description": "Серверная часть веб-приложения, отвечающая за выполнение бизнес-логики, хранение данных и обработку запросов клиентов.",
            "link": None
        },
        {
            "name": "Web-фреймворк",
            "description": "Программный каркас, предоставляющий набор инструментов для разработки, структурирования и сопровождения веб-приложений.",
            "link": "https://practicum.yandex.ru/blog/chto-takoe-framework/"
        },
        {
            "name": "SPA (Single Page Application)",
            "description": "Веб-приложение, взаимодействующее с пользователем без полной перезагрузки страницы; данные подгружаются динамически через сетевые запросы.",
            "link": "https://developer.mozilla.org"
        },
        {
            "name": "SSR (Server-Side Rendering)",
            "description": "Технология формирования HTML-страниц на стороне сервера, обеспечивающая снижение времени отображения и улучшение SEO-показателей.",
            "link": None
        },
        {
            "name": "CSR (Client-Side Rendering)",
            "description": "Технология рендеринга, при которой интерфейс страницы формируется браузером на основе JavaScript.",
            "link": "https://web.dev"
        },
        {
            "name": "REST",
            "description": "Архитектурный стиль построения веб-интерфейсов, основанный на принципах управления ресурсами через HTTP и stateless-взаимодействии.",
            "link": None
        },
        {
            "name": "API",
            "description": "Интерфейс взаимодействия компонентов системы, позволяющий клиенту выполнять операции над данными без доступа к внутренней реализации сервера.",
            "link": None
        },
        {
            "name": "HTTP",
            "description": "Протокол передачи гипертекстовой информации между клиентом и сервером в сети Интернет.",
            "link": "https://developer.mozilla.org"
        },
        {
            "name": "JSON",
            "description": "Текстовый формат обмена структурированными данными, широко применяемый в веб-приложениях.",
            "link": None
        },
        {
            "name": "DOM",
            "description": "Объектная модель HTML-документа, предоставляющая интерфейс для программного изменения структуры веб-страниц.",
            "link": "https://www.w3.org"
        },
        {
            "name": "WebSocket",
            "description": "Двунаправленный коммуникационный протокол, позволяющий устанавливать постоянное соединение между браузером и сервером.",
            "link": None
        }
    ]


    with Session(engine) as session:
        for term in initial_terms:
            if get_term_by_name(session, term["name"]) is None:
                create_term(session, TermCreate(**term))

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/", summary="Главная страница", description="Возвращает приветственное сообщение.")
def read_root():
    return {"message": "Welcome to the Glossary API!"}

@app.get("/terms", response_model=list[TermResponse], tags=["Terms"])
def get_terms():
    with Session(engine) as session:
        return get_all_terms(session)

@app.get("/glossary", response_class=HTMLResponse, summary="HTML-представление глоссария")
def glossary_page():
    with Session(engine) as session:
        terms = get_all_terms(session)

    items_html = ""
    for term in terms:
        link_html = ""
        if getattr(term, "link", None):
            link_html = f'<a href="{term.link}" class="term-link" target="_blank" rel="noopener noreferrer">Ссылка на источник</a>'

        items_html += f"""
        <article class="term-card">
            <h2 class="term-title">{term.name}</h2>
            <p class="term-description">{term.description}</p>
            {link_html}
        </article>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>Глоссарий терминов</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: #f5f5f7;
                color: #222;
            }}
            header {{
                background: #1f2933;
                color: #fff;
                padding: 16px 24px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            header h1 {{
                margin: 0;
                font-size: 20px;
            }}
            main {{
                max-width: 900px;
                margin: 24px auto 40px;
                padding: 0 16px;
            }}
            .term-list {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 16px;
            }}
            .term-card {{
                background: #fff;
                border-radius: 8px;
                padding: 16px 18px;
                box-shadow: 0 1px 3px rgba(15, 23, 42, 0.15);
                display: flex;
                flex-direction: column;
                gap: 8px;
            }}
            .term-title {{
                margin: 0;
                font-size: 18px;
                font-weight: 600;
                color: #111827;
            }}
            .term-description {{
                margin: 0;
                margin-bottom: auto;
                font-size: 14px;
                line-height: 1.5;
                color: #374151;
            }}
            .term-link {{
                margin-top: 8px;
                align-self: flex-start;
                font-size: 13px;
                text-decoration: none;
                color: #2563eb;
                padding: 4px 8px;
                border-radius: 4px;
                background-color: rgba(37, 99, 235, 0.08);
            }}
            .term-link:hover {{
                background-color: rgba(37, 99, 235, 0.16);
            }}
            .empty-state {{
                margin-top: 24px;
                font-size: 14px;
                color: #6b7280;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Глоссарий терминов</h1>
        </header>
        <main>
            {"<p class='empty-state'>Пока в глоссарии нет ни одного термина.</p>" if not terms else f"<section class='term-list'>{items_html}</section>"}
        </main>
    </body>
    </html>
    """

    return HTMLResponse(content=html)

@app.post("/terms", response_model=TermResponse)
def add_term(term: TermCreate):
    with Session(engine) as session:
        existing_term = get_term_by_name(session, term.name)
        if existing_term:
            raise HTTPException(status_code=400, detail="Term already exists")
        return create_term(session, term)

@app.put("/terms/{term_name}", response_model=TermResponse)
def edit_term(term_name: str, term: TermCreate):
    with Session(engine) as session:
        existing_term = get_term_by_name(session, term_name)
        if not existing_term:
            raise HTTPException(status_code=404, detail="Term not found")
        return update_term(session, term_name, term)

@app.delete("/terms/{term_name}")
def remove_term(term_name: str):
    with Session(engine) as session:
        existing_term = get_term_by_name(session, term_name)
        if not existing_term:
            raise HTTPException(status_code=404, detail="Term not found")
        delete_term(session, term_name)
        return {"message": "Term deleted successfully"}

