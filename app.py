import os
import asyncio
import aiohttp_cors
import aiohttp
import ujson


PORT = int(os.getenv("PORT", 8080))
app = aiohttp.web.Application()


async def proxy(request):
    body = await request.json()
    url = body.pop('url')

    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        response = await session.post(url, json=body)

        try:
            data = await response.json()
            return aiohttp.web.json_response(data)
        except:
            return aiohttp.web.Response(status=400)


(aiohttp_cors
 .setup(app, defaults={
     "*": aiohttp_cors.ResourceOptions(allow_credentials=True,
                                       expose_headers="*",
                                       allow_headers="*",)})
 .add(app.router.add_route("POST", "/", proxy)))


if __name__ == "__main__":
    aiohttp.web.run_app(app, port=PORT)
