import { Hono } from "hono";

const app = new Hono();
app.get("/", (c) => c.text("Hello World!"));
app.get("/niku", (c) => c.text("ごはんたべたい!"));

export default app;
