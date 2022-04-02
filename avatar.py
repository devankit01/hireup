import python_avatars as pa

# Completely random avatar
random_avatar_1 = pa.Avatar.random()
random_avatar_1.render("1.svg")
# Completely random avatar except for the hat
random_avatar_2 = pa.Avatar.random(top=pa.HatType.HAT)  # More attributes can stay fixed
random_avatar_2.render("2.svg")

# Fixed avatar but random clothes
random_avatar_3 = pa.Avatar(
    style=pa.AvatarStyle.CIRCLE,
    hair_color=pa.HairColor.BLACK,
    accessory=pa.AccessoryType.NONE,
    clothing=pa.ClothingType.pick_random(), # The clothes are chosen randomly
)
random_avatar_3.render("3.svg")
