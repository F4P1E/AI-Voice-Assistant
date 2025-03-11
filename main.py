# This code sets up a voice assistant using the LiveKit framework.
# It loads environment variables, imports necessary modules, and defines an asynchronous entry point function.
# The `entrypoint` function initializes the voice assistant's context and connects to the audio stream.
# It creates an instance of `AssistantFnc` to handle temperature control commands.
# The `VoiceAssistant` is configured with voice activity detection (VAD), speech-to-text (STT), language model (LLM), and text-to-speech (TTS) components.
# The assistant starts listening in the specified room and greets the user.
# The script runs the application using the `cli.run_app` method with the defined entry point function.

import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )
    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("Hey, how can I help you today!", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))