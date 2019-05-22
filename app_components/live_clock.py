import datetime
import dash_html_components as html
import base64

def get_clock(t=datetime.datetime.now()):
    clock_style = {"color": "#4286f4", "textAlign": "center", "font-size": "2rem"}
    return html.Div([
            html.Br(),
            html.P(
                t.strftime("%H:%M:%S"),
                id="live_clock",
                className="six columns",
                style=clock_style,
            )],
            className='six columns'
        )

def get_logo():
    image = "images/cj_logo.png"
    encoded_image = base64.b64encode(open(image, "rb").read())
    logo = html.Div(
        html.Img(
            src="data:image/png;base64,{}".format(encoded_image.decode()), height="70"
        ),
        style={"marginTop": "0"},
        className="six columns",
    )
    return logo