import os
import re
from os import listdir
from os.path import isfile, join
from abc import abstractmethod
import unittest


# 1
class DependencyHelper:
    def __init__(self):
        self.adj = {}

    def add(self, a, b):
        self.adj[b] = self.adj.get(b, set())
        self.adj[a] = self.adj.get(a, set())
        self.adj[b].add(a)

    def __add__(self, pair):
        (a, b) = pair
        self.add(a, b)
        return self

    def __sub__(self, pair):
        (a, b) = pair
        self.remove(a, b)
        return self

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __bool__(self):
        keys = list(self.adj.keys())
        if keys:
            return not self.dfs(keys[0], {})
        else:
            return True

    def update(self, dh):
        assert isinstance(dh, DependencyHelper)
        for k in dh.adj:
            v = dh.adj[k]
            self.adj[k] = self.adj.get(k, set())
            self.adj[k] |= v

    def remove(self, a, b):
        assert a is not None and b is not None
        self.adj[b] = self.adj.get(b, set())
        self.adj[b].remove(a)

    def dfs(self, node, visited):
        assert node is not None
        visited.setdefault(node, 1)
        for child in self.adj.get(node, []):
            if visited.get(child, 0) == 0:
                if self.dfs(child, visited):
                    return True
            elif visited.get(child, 0) == 1:
                return True
        visited.setdefault(node, 2)

        return False

    def get_dependent(self, a):
        d = []
        for k in self.adj:
            if a in self.adj[k]:
                d.append(k)
        return d

    def has_cycle_dependency(self):
        return bool(self)


# 2
class PriorityHelper(DependencyHelper):
    def enumerate_priorities(self):
        priorities = {}
        for k in self.adj:
            m = -1
            for i in self.adj[k]:
                i_p = priorities.get(i, 0)
                if i_p > m:
                    m = i_p
            priorities.setdefault(k, m + 1)

        return priorities


# 3
# Collects all files from root_dir (even internal ones!)
class WalkClass(DependencyHelper):
    def __init__(self, root_dir, file_pattern=None):
        assert isinstance(root_dir, str) and len(root_dir) > 0
        super().__init__()
        self.files = []
        for top, dirs, files in os.walk(root_dir):
            for nm in files:
                path = os.path.join(top, nm)
                if file_pattern is not None:
                    if re.match(file_pattern, nm):
                        self.files.append(path)
                else:
                    self.files.append(path)

    @abstractmethod
    def handle_files(self, root_dir, files):
        pass


# 3
class MakeFilesHandler(DependencyHelper):
    def __init__(self, root_dir):
        assert isinstance(root_dir, str) and len(root_dir) > 0
        super().__init__()
        self.filename = 'make'
        self.handle_files(root_dir)

    @staticmethod
    def add_files(lines, instruction):
        start = next((i for i, e in enumerate(lines) if e.startswith(instruction)), None)
        files = []
        if start is not None:
            i = start + 1
            while lines[i].find(')') == -1:
                files.append(lines[i].lstrip().rstrip())
                i += 1
        return files

    def handle_files(self, root_dir):
        peerdirs = []
        includes = []
        files = [f for f in listdir(root_dir) if isfile(join(root_dir, f)) and f == self.filename]
        for filename in files:
            with open(join(root_dir, filename), 'r') as f:
                lines = f.readlines()
                peerdirs += MakeFilesHandler.add_files(lines, 'PEERDIR')
                includes += MakeFilesHandler.add_files(lines, 'INCLUDE')

        for p in peerdirs:
            self.add(join(p, self.filename), join(root_dir, self.filename))
            self.handle_files(p)


class TestDependencyMethods(unittest.TestCase):
    def test_add(self):
        dependency_helper = DependencyHelper()
        dependency_helper.add(1, 2)
        self.assertEqual({2: {1}, 1: set()}, dependency_helper.adj)

    def test_plus(self):
        dependency_helper = DependencyHelper()
        dependency_helper += (1, 2)
        self.assertEqual({2: {1}, 1: set()}, dependency_helper.adj)

    def test_priority(self):
        ph = PriorityHelper()
        ph += (1, 2)
        ph += (1, 3)
        ph += (4, 3)
        self.assertEqual({2: 1, 1: 0, 3: 1, 4: 0}, ph.enumerate_priorities())

    def test_cycle(self):
        dependency_helper = DependencyHelper()
        dependency_helper.add(1, 2)
        dependency_helper.add(2, 1)
        self.assertFalse(bool(dependency_helper))

    def test_remove(self):
        dependency_helper = DependencyHelper()
        dependency_helper += (1, 2)
        dependency_helper += (4, 20)
        dependency_helper -= (4, 20)
        self.assertEqual({2: {1}, 1: set(), 4: set(), 20: set()}, dependency_helper.adj)

    def test_update(self):
        dependency_helper = DependencyHelper()
        dependency_helper2 = DependencyHelper()
        dependency_helper += (1, 2)
        dependency_helper2 += (1, 4)
        dependency_helper2 += (3, 2)
        dependency_helper.update(dependency_helper2)
        self.assertEqual({2: {1, 3}, 1: set(), 3: set(), 4: {1}}, dependency_helper.adj)


unittest.main()