defmodule Cookie do
  @content """
  Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
  Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
  Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
  Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8
  """

  @test_content """
  Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
  Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
  """
  def run(input) do
    contents =
      if input == :test do
        cont(@test_content)
      else
        cont(@content)
      end

    spec =
      contents
      |> Enum.into(%{}, &to_map/1)

    ingredients = Map.keys(spec)

    initial =
      ingredients
      |> Enum.map(fn x -> %{x => 1} end)
      |> IO.inspect()

    make(ingredients, 99, spec, initial)
    |> Enum.map(&counter(&1, spec))
  end

  def counter(ingredient_map, spec) do
    ingredients = Map.keys(ingredient_map)

    c =
      Enum.map(ingredients, fn ingredient ->
        measure(ingredient, spec, :capacity, ingredient_map)
      end)
      |> Enum.sum()
      |> pick

    d =
      Enum.map(ingredients, fn ingredient ->
        measure(ingredient, spec, :durability, ingredient_map)
      end)
      |> Enum.sum()
      |> pick

    f =
      Enum.map(ingredients, fn ingredient ->
        measure(ingredient, spec, :flavor, ingredient_map)
      end)
      |> Enum.sum()
      |> pick

    t =
      Enum.map(ingredients, fn ingredient ->
        measure(ingredient, spec, :texture, ingredient_map)
      end)
      |> Enum.sum()
      |> pick

    calories =
      Enum.map(ingredients, fn ingredient ->
        measure(ingredient, spec, :calories, ingredient_map)
      end)
      |> Enum.sum()
      |> pick

    {c * d * f * t, calories}
  end

  def pick(num) do
    if num < 0 do
      0
    else
      num
    end
  end

  def measure(ing, spec, key, ingredient_map) do
    ingredient_map[ing] * spec[ing][key]
  end

  def make(_ingredients, 0, _spec, res) do
    res
  end

  def make(ingredients, n, spec, res) do
    new_res =
      for ingredient <- ingredients, x <- res do
        case Map.get(x, ingredient) do
          nil -> Map.put(x, ingredient, 1)
          val -> Map.put(x, ingredient, val + 1)
        end
      end

    new_res = new_res |> Enum.uniq()

    make(ingredients, n - 1, spec, new_res)
  end

  def cont(contents) do
    contents
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.map(&parse/1)
  end

  @re ~r/(?<ingredient>\w+):\scapacity\s(?<capacity>-?\d+),\sdurability\s(?<durability>-?\d+),\sflavor\s(?<flavor>-?\d+),\stexture\s(?<texture>-?\d+),\scalories\s(?<calories>-?\d+)/
  def parse(string) do
    Regex.named_captures(@re, string)
  end

  def to_map(%{
        "calories" => cal,
        "capacity" => cap,
        "durability" => dur,
        "flavor" => fl,
        "ingredient" => ingredient,
        "texture" => tx
      }) do
    {
      ingredient,
      %{
        calories: String.to_integer(cal),
        capacity: String.to_integer(cap),
        durability: String.to_integer(dur),
        flavor: String.to_integer(fl),
        texture: String.to_integer(tx)
      }
    }
  end
end

Cookie.run(:test)
|> Enum.max_by(fn x -> elem(x, 0) end)
|> IO.inspect()

Cookie.run(:prod)
|> Enum.max_by(fn x -> elem(x, 0) end)
|> IO.inspect()

Cookie.run(:prod)
|> Enum.filter(fn x -> elem(x, 1) == 500 end)
|> Enum.max()
|> IO.inspect()
