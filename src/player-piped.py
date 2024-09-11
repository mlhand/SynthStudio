import audiogen
import sys

beats = audiogen.util.mixer(
        (audiogen.tone(440), audiogen.tone(445)),
        [(audiogen.util.constant(1), audiogen.util.constant(1)),]
)

audiogen.sampler.write_wav(sys.stdout, beats)
