import enum
import colour
import numpy

RgbColorspace = colour.RGB_Colourspace

sRGB_COLORSPACE = colour.models.RGB_COLOURSPACE_sRGB


class ChromaticAdaptationTransform(enum.Enum):
    # values can only be ones supported by ``colour``
    # >>> print("\n".join(colour.CHROMATIC_ADAPTATION_TRANSFORMS))
    bianco_2010 = "Bianco 2010"
    bianco_pc_2010 = "Bianco PC 2010"
    bradford = "Bradford"
    CAT02_Brill = "CAT02 Brill 2008"
    CAT02 = "CAT02"
    CAT16 = "CAT16"
    CMCCAT2000 = "CMCCAT2000"
    CMCCAT97 = "CMCCAT97"
    fairchild = "Fairchild"
    sharp = "Sharp"
    von_kries = "Von Kries"
    XYZ_scaling = "XYZ Scaling"

    @classmethod
    def get_default(cls):
        return cls.bradford


def get_available_colorspaces() -> list[str]:
    # copied from colour.models.RGB_COLORSPACES.keys() but we removed the aliases
    return [
        "ACES2065-1",
        "ACEScc",
        "ACEScct",
        "ACEScg",
        "ACESproxy",
        "ARRI Wide Gamut 3",
        "ARRI Wide Gamut 4",
        "Adobe RGB (1998)",
        "Adobe Wide Gamut RGB",
        "Apple RGB",
        "Best RGB",
        "Beta RGB",
        "Blackmagic Wide Gamut",
        "CIE RGB",
        "CIE XYZ-D65 - Scene-referred",
        "Cinema Gamut",
        "ColorMatch RGB",
        "DCDM XYZ",
        "DCI-P3",
        "DCI-P3-P",
        "DJI D-Gamut",
        "DRAGONcolor",
        "DRAGONcolor2",
        "DaVinci Wide Gamut",
        "Display P3",
        "Don RGB 4",
        "EBU Tech. 3213-E",
        "ECI RGB v2",
        "ERIMM RGB",
        "Ekta Space PS 5",
        "F-Gamut",
        "F-Gamut C",
        "FilmLight E-Gamut",
        "FilmLight E-Gamut 2",
        "Gamma 1.8 Encoded Rec.709",
        "Gamma 2.2 Encoded AP1",
        "Gamma 2.2 Encoded AdobeRGB",
        "Gamma 2.2 Encoded Rec.709",
        "ITU-R BT.2020",
        "ITU-R BT.470 - 525",
        "ITU-R BT.470 - 625",
        "ITU-R BT.709",
        "ITU-T H.273 - 22 Unspecified",
        "ITU-T H.273 - Generic Film",
        "Linear AdobeRGB",
        "Linear P3-D65",
        "Linear Rec.2020",
        "Linear Rec.709 (sRGB)",
        "Max RGB",
        "N-Gamut",
        "NTSC (1953)",
        "NTSC (1987)",
        "P3-D65",
        "PLASA ANSI E1.54",
        "Pal/Secam",
        "ProPhoto RGB",
        "Protune Native",
        "REDWideGamutRGB",
        "REDcolor",
        "REDcolor2",
        "REDcolor3",
        "REDcolor4",
        "RIMM RGB",
        "ROMM RGB",
        "Russell RGB",
        "S-Gamut",
        "S-Gamut3",
        "S-Gamut3.Cine",
        "SMPTE 240M",
        "SMPTE C",
        "Sharp RGB",
        "V-Gamut",
        "Venice S-Gamut3",
        "Venice S-Gamut3.Cine",
        "Xtreme RGB",
        "sRGB",
        "sRGB Encoded AP1",
        "sRGB Encoded P3-D65",
        "sRGB Encoded Rec.709 (sRGB)",
    ]


def get_colorspace(name: str) -> RgbColorspace | None:
    return colour.models.RGB_COLOURSPACES.get(name)


def colorspace_to_colorspace(
    array: numpy.ndarray,
    source_colorspace: RgbColorspace,
    target_colorspace: RgbColorspace,
    chromatic_adaptation_transform: ChromaticAdaptationTransform | None = None,
) -> numpy.ndarray:

    cat = chromatic_adaptation_transform or ChromaticAdaptationTransform.get_default()

    return colour.models.RGB_to_RGB(
        array,
        input_colourspace=source_colorspace,
        output_colourspace=target_colorspace,
        chromatic_adaptation_transform=cat.value,
        apply_cctf_decoding=True,
        apply_cctf_encoding=True,
    )


def is_colorspace_decoding_linear(colorspace: RgbColorspace) -> bool:
    return (
        colorspace.cctf_decoding is None
        or colorspace.cctf_decoding == colour.linear_function
    )
