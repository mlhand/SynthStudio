import audiogen

beats = audiogen.util.mixer(
        (audiogen.tone(440), audiogen.tone(445)),
        [(audiogen.util.constant(1), audiogen.util.constant(1)),]
)

with open("output.wav", "wb") as f:
    audiogen.sampler.write_wav(f, beats)
