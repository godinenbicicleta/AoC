package day08

import (
	"bufio"
	"os"
	"strconv"
)

func Sum(nums []int) int {
	res := 0
	for _, elem := range nums {
		res += elem
	}
	return res
}

type Node struct {
	childs    []*Node
	metadatas []int
}

func buildTree(fname string) *Node {
	f, err := os.Open(fname)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanWords)
	nums := []int{}
	for scanner.Scan() {
		w := scanner.Text()
		num, err := strconv.Atoi(w)
		if err != nil {
			panic(err)
		}
		nums = append(nums, num)
	}

	index := 0

	node := Node{childs: []*Node{}, metadatas: []int{}}
	Parse(nums, index, &node)
	return &node

}

func Solve(fname string) int {
	tree := buildTree(fname)
	return SumMetadata(tree)
}
func Solve2(fname string) int {
	tree := buildTree(fname)
	return SumTree(tree)
}

func SumTree(node *Node) int {
	total := 0
	if len(node.childs) == 0 {
		for _, v := range node.metadatas {
			total += v
		}
		return total
	}

	for _, v := range node.metadatas {
		ix := v - 1
		if ix >= 0 && ix < len(node.childs) {
			total += SumTree(node.childs[ix])
		}
	}
	return total
}

func SumMetadata(node *Node) int {
	total := 0
	for _, v := range node.metadatas {
		total += v
	}
	for _, child := range node.childs {
		total += SumMetadata(child)
	}
	return total
}

func Parse(nums []int, index int, node *Node) int {
	num_childs := nums[index]
	index++
	num_metadatas := nums[index]
	index++
	for j := 0; j < num_childs; j++ {
		child_node := Node{childs: []*Node{}, metadatas: []int{}}
		index = Parse(nums, index, &child_node)
		node.childs = append(node.childs, &child_node)
	}
	metadatas := []int{}
	for j := 0; j < num_metadatas; j++ {
		metadatas = append(metadatas, nums[index])
		index++
	}
	node.metadatas = metadatas
	return index
}
