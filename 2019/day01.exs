defmodule Fuel do
  def from_mass(mass) do
    req = div(mass, 3) - 2

    if req > 0 do
      req
    else
      0
    end
  end

  def from_mass_req(mass) do
    req = div(mass, 3) - 2

    if req > 0 do
      req + from_mass_req(req)
    else
      0
    end
  end

  def for_file(file, mass_func) do
    File.stream!(file)
    |> Enum.reduce(0, fn elem, acc ->
      fuel =
        String.trim(elem)
        |> String.to_integer()
        |> mass_func.()

      acc + fuel
    end)
  end
end

Fuel.for_file("input01.txt", &Fuel.from_mass(&1))
|> IO.puts()

Fuel.for_file("input01.txt", &Fuel.from_mass_req(&1))
|> IO.puts()

Fuel.from_mass_req(1969)
|> IO.puts()
