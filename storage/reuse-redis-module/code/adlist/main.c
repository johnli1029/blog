#include <assert.h>
#include <stdlib.h>
#include "adlist.h"

void create_a_empty_list(void)
{
    // 创建一个新链表
    list* l = listCreate();

    // 检查表头和表尾
    assert(
        l->head == NULL &&
        l->tail == NULL
    );

    // 检查节点数量
    assert(
        l->len == 0
    );

    // 检查类型限定函数
    assert(
        l->dup == NULL &&
        l->free == NULL &&
        l->match == NULL
    );

    // 释放链表
    listRelease(l);
}

void add_node_to_list(void)
{
    int one = 1,
        two = 2,
        three = 3;

    list* l = listCreate();

    // l = [1]
    listAddNodeHead(l, &one);

    // l = [1, 3]
    listAddNodeTail(l, &three);

    // l = [1, 2, 3]
    listNode* node = listSearchKey(l, &one);
    listInsertNode(l, node, &two, 1);  // insert 2 after 1

    // current 现在包含值 1 
    listNode* current = listFirst(l);
    assert(
        current->value == &one
    );

    // current 现在包含值 2
    current = listNextNode(current);
    assert(
        current->value == &two
    );

    // current 现在包含值 3
    current = listNextNode(current);
    assert(
        current->value == &three
    );

    // 释放
    listRelease(l);
}

void test_iterator(void)
{
    int one = 1,
        two = 2,
        three = 3;

    // l = [1, 2, 3]
    list* l = listCreate();
    listAddNodeTail(l, &one);
    listAddNodeTail(l, &two);
    listAddNodeTail(l, &three);

    // 取得一个从表头向表尾迭代的迭代器
    listIter* itertor = listGetIterator(l, AL_START_HEAD);
    listNode* current;
    
    // 第一个节点
    current = listNext(itertor);
    assert(
        current->value == &one
    );

    // 第二个节点
    current = listNext(itertor);
    assert(
        current->value == &two
    );

    // 第三个节点
    current = listNext(itertor);
    assert(
        current->value == &three
    );

    // 释放
    listRelease(l);
    listReleaseIterator(itertor);
}

void main(void)
{
    create_a_empty_list();

    add_node_to_list();

    test_iterator();
}
