defmodule Short do
  def get_distances(file) do
    file
    |> File.read!()
    |> parse
  end

  def parse(string) do
    string
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.map(&parse_route/1)
    |> List.flatten()
    |> Enum.into(%{})
  end

  def parse_route(string) do
    # Tambi to Straylight = 107
    captures = Regex.named_captures(~r/(?<from>\w+)\sto\s(?<to>\w+)\s=\s(?<distance>\d+)/, string)
    distance = String.to_integer(captures["distance"])

    [
      {{captures["from"], captures["to"]}, distance},
      {{captures["to"], captures["from"]}, distance}
    ]
  end
end
