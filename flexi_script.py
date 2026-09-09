Import("env")

# Custom HEX from ELF
env.AddPostAction(
    "$BUILD_DIR/${PROGNAME}.elf",
    env.VerboseAction(" ".join([
        "$OBJCOPY", "-O", "ihex", "-R", ".eeprom", 
        '"$BUILD_DIR/${PROGNAME}.elf"', '"$BUILD_DIR/${PROGNAME}.hex"'
    ]), "Building $BUILD_DIR/${PROGNAME}.hex")
)

# Custom UF2 from BIN (quote paths — workspace may contain spaces)
def after_build(source, target, env):
    build_dir = env.subst("$BUILD_DIR")
    prog = env.subst("${PROGNAME}")
    bin_path = f"{build_dir}/{prog}.bin"
    uf2_path = f"{build_dir}/{prog}.uf2"
    print(f"Building {uf2_path}")
    env.Execute(
        f'python uf2conv.py -c -b 0x08010000 -f 0x57755a57 "{bin_path}" --output "{uf2_path}"'
    )

env.AddPostAction("buildprog", after_build)