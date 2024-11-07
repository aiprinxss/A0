builder = Builder::XmlMarkup.new(:target=>STDOUT, :indent=>2)
builder.person { |b| b.name("UNKNOWN"); b.phone("456-1234") }
