defmodule Day06 do
  # @p1_test [{7, 9}, {15, 40}, {30, 200}]
  @p1 [{56, 546}, {97, 1927}, {78, 1131}, {75, 1139}]
  def p1 do
    @p1
    |> Enum.map(&solve/1)
    |> Enum.product()
  end

  def p2_test do
    solve({71530, 940_200})
  end

  def p2 do
    solve({56_977_875, 546_192_711_311_139})
  end

  def solve({time, record}) do
    time
    |> to_distances()
    |> Enum.count(&(&1 > record))
  end

  def to_distances(time) do
    Enum.map(0..time, fn v -> v * (time - v) end)
  end
end
