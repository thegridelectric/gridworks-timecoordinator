# gridworks-timecoordinator

The GridWorks **time coordinator**: the authority for simulated time in a
GridWorks world. It broadcasts `sim.timestep` messages over a RabbitMQ
broker; every GridWorks actor built on
[gridworks-base](https://github.com/thegridelectric/gridworks-base) already
tracks simulated time from these broadcasts and can answer with `Ready`
when it has processed up to the announced time.

A time coordinator is not a GNode — it is an orchestration participant,
like a supervisor — but its alias (e.g. `d1.tc`) lives in the GNode tree,
anticipating a tree of time coordinators that work with each other.

## Status

Early — rebuilt from scratch on gridworks-base. The previous generation of
this repo is preserved on the `legacy` branch. Current contents: `tc-hello`,
a hello-world coordinator that broadcasts timesteps at a fixed wall-clock
cadence, advancing simulated time by a configurable step per beat (so
simulated time can already run faster than wall time). The Ready barrier —
advancing only when all expected participants have reported — is the next
stage, not this one.

## Development

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```shell
uv sync
uv run pytest
uv run tc-hello --beat-seconds 5 --step-seconds 60
```

`tc-hello` connects to the broker at `GWBASE_RABBIT__URL` (default: a local
dev rabbit at `amqp://smqPublic:smqPublic@localhost:5672/d1__1`).
